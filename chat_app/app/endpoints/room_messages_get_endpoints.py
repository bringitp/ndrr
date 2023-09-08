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
    return skeltone_get_current_user(Authorization, db, public_key)


@router.get("/room/{room_id}/messages", response_model=Dict[str, Any])
async def get_room_messages(
    room_id: int,
    skip: int = 0,
    limit: int = 50,
    login_user: LoginUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    room = db.query(Room).get(room_id)
    # Check if the user is a member of the room
    if (
        not db.query(RoomMember)
        .filter_by(room_id=room_id, user_id=login_user.id)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this room",
        )

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )

    if room.over_karma_limit < login_user.karma and room.over_karma_limit != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="More karma needed"
        )

    if room.under_karma_limit < login_user.karma and room.under_karma_limit != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="More real needed"
        )

    # メンバー情報を一括で取得
    room_members = db.query(RoomMember).filter(RoomMember.room_id == room_id).all()

    user_avatar_urls = (
        db.query(User.id, AvatarList.avatar_url)
        .filter(User.avatar_id == AvatarList.avatar_id)
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
    # vital_member_info から user_id と avatar_url の対応を作成
    user_id_to_avatar_url = {
        member["user_id"]: member["avatar_url"] for member in vital_member_info
    }
    # ルーム情報を取得
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
       "version": "0.02",
   }
    # private message 取得
    # normal message 取得
    normal_messages = (
        db.query(Message)
        .options(joinedload(Message.sender).load_only("avatar_id"))
        .filter((Message.room_id == room_id) & (~Message.sender_id.in_(block_list)))
        .order_by(Message.sent_at.desc())
        .offset(skip)
        .limit(min(limit, 30))
        .all()
    )
    # private messageのIDと normal massage のIDをかぶらないようにする

    all_messages = sorted(
        normal_messages,
        key=lambda message: message.sent_at,
        reverse=True,
    )

    for message in all_messages:
        sender_id = message.sender_id
        sender_avatar_id_and_url = next(
            (
                avatar_url
                for user_id, avatar_url in user_avatar_urls
                if user_id == sender_id
            ),
            None,
        )
        print (message.id)

        # senderを再度取得
        sender = db.query(User).filter(User.id == sender_id).first()

        if sender:
            message_data = {
                "id": message.id,
                "content": message.content,
                "toxicity": message.toxicity,
                "sentiment": message.sentiment,
                "fluence": message.fluence,
                "sent_at": message.sent_at.strftime("%y-%m-%d %H:%M:%S"),
                "sender": {
                    "username": escape_html(sender.username),
                    "user_id": sender.id,
                    "avatar_url": sender_avatar_id_and_url,  # 修正: sender_avatar_urlを使用
                    "trip": escape_html(sender.trip),
                    "karma": sender.karma,
                    "privilege": sender.privilege,
                    "lastlogin_at": sender.lastlogin_at.strftime("%m-%d %H:%M"),
                    "penalty_points": sender.penalty_points,
                    "profile": escape_html(sender.profile),
                    "sender_id": message.sender_id if message.message_type == "private" else None,
                    "receiver_id": message.receiver_id if message.message_type == "private" else None,
                    "receiver_username": "all",
                },
                "is_private": (message.message_type == "private"),
            }

            response_data["messages"].append(message_data)

    return response_data
