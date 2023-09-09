from fastapi import FastAPI, Depends, Header, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from chat_app.app.database.models import (
    Message,
    Room,
    User,
    RoomMember,
    AvatarList,
    UserNGList,
)
from sqlalchemy.orm import joinedload
from typing import Dict, Any
from datetime import datetime, timedelta
import requests
import jwt
from janome.tokenizer import Tokenizer
from collections import defaultdict
import html
import functools
import time
from chat_app.app.utils import (
    create_db_engine_and_session,
    get_public_key,
    escape_html,
)
from chat_app.app.auth_utils import (
    UserToken,
    LoginUser,
    validate_token,
    get_user_by_sub,
    skeltone_get_current_user,
    get_block_list,
)
from cachetools import TTLCache
# キャッシュの設定（20秒のTTLキャッシュ）
cache = TTLCache(maxsize=1000, ttl=120)

# データベース関連の初期化
engine, SessionLocal, Base = create_db_engine_and_session()
public_key = get_public_key("https://ron-the-rocker.net/auth", "ndrr")
# Janomeのトークナイザーの初期化
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    Authorization: str = Header(None), db: Session = Depends(get_db)
) -> User:
    # キャッシュからユーザー情報を取得
    cached_user = cache.get(Authorization)
    if cached_user:
        return cached_user

    # キャッシュにない場合はデータベースからユーザー情報を取得
    user = skeltone_get_current_user(Authorization, db, public_key)
    # ユーザー情報をキャッシュに保存
    cache[Authorization] = user

    return user


@router.get("/room/{room_id}/messages", response_model=Dict[str, Any])
async def get_room_messages(
    room_id: int,
    login_user: LoginUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    room = db.query(Room).get(room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )
    # Check if the user is a member of the room
    # ログインユーザーがルームのメンバーであるかを確認し、メンバー情報を一括で取得
    room_members = (
        db.query(RoomMember)
        .filter(RoomMember.room_id == room_id)
        .options(joinedload(RoomMember.user))  # ユーザー情報を一括で取得
        .all()
    )

    # ログインユーザーがルームのメンバーであるかを確認
    user_ids_in_room = [room_member.user_id for room_member in room_members]
    if login_user.id not in user_ids_in_room:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this room",
        )

    if room.over_karma_limit < login_user.karma and room.over_karma_limit != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="More karma needed"
        )

    if room.under_karma_limit < login_user.karma and room.under_karma_limit != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="More reality needed"
        )

    # room_membersからavatar_idのリストを取得
    avatar_ids = [room_member.user.avatar_id for room_member in room_members]

    # AvatarListから対応するavatar_idのレコードを取得
# AvatarListとUserテーブルを結合し、avatar_idを用いて結合条件を指定
    user_avatar_urls = (
        db.query(User.id, AvatarList.avatar_url)
        .join(AvatarList, User.avatar_id == AvatarList.avatar_id)
        .filter(User.id.in_(avatar_ids))  # avatar_idsに含まれるユーザーIDに絞り込み
        .all()
    )

    vital_member_info = []
    blocked_user_ids = set()  # ブロック済みユーザーのIDをセットで保持
    block_list = get_block_list(login_user.id, db)

    for room_member in room_members:
        user = room_member.user
        avatar_id_and_url = next(
            (
                avatar_url
                for user_id, avatar_url in user_avatar_urls
                if user_id == user.id
            ),
            None,
        )
        # ブロック済みユーザーかどうかを確認
        blocked = user.id in block_list  # block_listに含まれているかどうかを確認
        if blocked:
            blocked_user_ids.add(user.id)
        vital_member_info.append(
            {
                "user_id": user.id,
                "username": user.username,
                "avatar_url": avatar_id_and_url,
                "blocked": bool(blocked),
                "ami": bool(user.id == login_user.id),
            }
        )

    # ルームオーナー情報を取得
    room_owner = db.query(User.username).filter(User.id == room.owner_id).first()
    response_data = {
        "room": {
            "room_id": room.id,
            "room_label": room.label,
            "room_name": room.name,
            "room_member_count": len(vital_member_info),  # メンバー情報の数を使う
            "room_owner_id": room.owner_id,
            "room_login_user_name": login_user.username,
            "room_login_user_id": login_user.id,
            "room_owner_name": room_owner.username,
            "room_max_capacity": room.max_capacity,
            "room_restricted_karma_over_limit": room.over_karma_limit,
            "room_restricted_karma_under_limit": room.under_karma_limit,
            "room_lux": room.lux,
        },
        "room_members": vital_member_info,  # 部屋の現在のメンバー
        "messages": [],
        "version": "0.03",
    }
    # normal message 取得
    normal_messages = (
        db.query(Message)
        .filter(
            (Message.room_id == room_id) & (~Message.sender_id.in_(blocked_user_ids))
        )
        .order_by(Message.sent_at.desc())
        .limit(30)
        .all()
    )

    all_messages = sorted(
       normal_messages,
       key=lambda message: message.sent_at,
       reverse=True,
    )

    for message in all_messages:
        message_data = {
            "id": message.id,
            "content": message.content,
            "toxicity": message.toxicity,
            "sentiment": message.sentiment,
            "fluence": message.fluence,
            "sent_at": message.sent_at.strftime("%y-%m-%d %H:%M:%S"),
            "sender": {
                "username": message.signature_writer_name,
                "user_id": message.sender_id,
                "avatar_url": message.signature_avatar_url,  # 修正: sender_avatar_urlを使用
                "trip": message.signature_trip,
                "karma": message.signature_karma,
                "profile": message.signature_profile,
                "sender_id": message.sender_id
                if message.message_type == "private"
                else None,
                "receiver_id": message.receiver_id
                if message.message_type == "private"
                else None,
                "receiver_username": message.signature_recipient_name,
            },
            "is_private": (message.message_type == "private"),
        }

        response_data["messages"].append(message_data)

    return response_data
