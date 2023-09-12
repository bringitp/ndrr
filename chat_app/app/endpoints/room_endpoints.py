from fastapi import (
    FastAPI,
    Depends,
    Header,
    HTTPException,
    status,
    APIRouter,
    Request,
    BackgroundTasks,
)
from sqlalchemy.orm import Session
from chat_app.app.utils import create_db_engine_and_session, load_ng_words
from chat_app.app.database.models import Message, Room, User, RoomMember, AvatarList
from typing import Dict, Any
from datetime import datetime, timedelta
import requests
import jwt
from janome.tokenizer import Tokenizer
from collections import defaultdict
import html
import re
from sqlalchemy.sql import func
from chat_app.app.utils import create_db_engine_and_session, get_public_key, escape_html
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
ng_words = load_ng_words()  # ng word 読み込み
# JWT関連の設定
public_key = get_public_key("https://ron-the-rocker.net/auth", "ndrr")

# Janomeのトークナイザーの初期化
t = Tokenizer()
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


@router.post("/room/create", response_model=Dict[str, Any])
async def create_room(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = await request.json()
    # Create a new room
    new_room = Room(
        name=data.get("name"),
        label=data.get("label"),
        owner_id=current_user.id,
        room_type=data.get("room_type", "public"),
        room_password=data.get("room_password", ""),
        max_capacity=data.get("max_capacity", 20),
        over_karma_limit=data.get("over_karma_limit", 0),
        under_karma_limit=data.get("under_karma_limit", 0),
        lux=data.get("lux", 0),
        status="active",
        last_activity=datetime.now(),
    )


    db.add(new_room)
    db.commit()

    response_data = {
        "message": "Room created successfully",
        "room_id": new_room.id,
    }
    return response_data


@router.delete("/room/{room_id}/destroy", response_model=Dict[str, Any])
async def destroy_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # ルームをデータベースから取得
    room = db.query(Room).filter(Room.id == room_id).first()

    # ルームが存在しない場合、404エラーを返す
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # ユーザーがルームのオーナーでない場合、403エラーを返す
    if room.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not the owner of this room"
        )

    # ルームに参加している全てのメンバーを退出させる
    db.query(RoomMember).filter(RoomMember.room_id == room_id).delete()

    # ルームを削除
    db.delete(room)
    db.commit()

    return {"message": "Room deleted successfully"}


@router.post("/room/{room_id}", response_model=Dict[str, Any])
async def create_room_message(
    room_id: int,
    request: Request,
    login_user: LoginUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    data = await request.json()
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )

    # ユーザーがメンバーでない場合、403エラーを返す
    room_member = (
        db.query(RoomMember).filter_by(room_id=room_id, user_id=login_user.id).first()
    )
    if not room_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this room",
        )

    # ルームを取得
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )

    # ログインユーザーがルームの管理者でない場合、403エラーを返す
    if room.owner_id != login_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this room",
        )

    # 新しい部屋名を設定
    room.name = message_content = data.get("room_name")
    room.max_capacity = data.get("max_capacity")
    room.label = data.get("room_label")
    # データベースに変更をコミット
    db.commit()

    response_data = {"message": "Room name changed successfully"}
    return response_data


@router.put("/room/{room_id}/remove_member", response_model=dict)
async def remove_room_member(
    room_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = await request.json()
    member_id = message_content = data.get("member_id")

    # ユーザーが部屋のオーナーかどうかを確認
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if room.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not the owner of this room"
        )

    # メンバーを部屋から削除
    member = (
        db.query(RoomMember)
        .filter(RoomMember.room_id == room_id, RoomMember.user_id == member_id)
        .first()
    )
    if not member:
        raise HTTPException(status_code=404, detail="Member not found in the room")

    db.delete(member)
    db.commit()
    return {"message": "Member removed from the room successfully"}


@router.put("/room/{room_id}/depart_me", response_model=dict)
async def remove_room_member(
    room_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = await request.json()
    member_id = data.get("member_id")

    # ユーザーが部屋のオーナーかどうかを確認
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # メンバーを部屋から削除
    member = (
        db.query(RoomMember)
        .filter(RoomMember.room_id == room_id, RoomMember.user_id == member_id)
        .first()
    )
    if not member:
        raise HTTPException(status_code=404, detail="Member not found in the room")

    # ユーザーが部屋から出る場合
    if member_id == current_user.id:
        db.delete(member)
    else:
        # ユーザーが他のユーザーにオーナー権限を移行する場合
        db.delete(member)

    # ログアウトしたユーザーがオーナーだった場合、新しいオーナーを設定
    if current_user.id == room.owner_id:
        # 部屋の滞在時間が一番長いメンバーを見つける
        longest_stay_member = (
            db.query(RoomMember)
            .filter(
                RoomMember.room_id == room_id, RoomMember.user_id != current_user.id
            )
            .order_by(RoomMember.joined_at.desc())
            .first()
        )

        if longest_stay_member:
            room.owner_id = longest_stay_member.user_id
        else:
            # オーナーである自分以外のメンバーがいない場合は、オーナーを削除
            room.owner_id = None
            # ルームを削除
            db.delete(room)
            db.commit()
            return {"message": "Room deleted successfully"}
                    # その後部屋を削除

        if longest_stay_member:
            room.owner_id = longest_stay_member.user_id

    system = db.query(User).filter(User.id == 1).first()
    avatar_url = (
        db.query(AvatarList.avatar_url)
        .filter_by(avatar_id=current_user.avatar_id)
        .scalar()
    )

    new_message = Message(
        content=f"{current_user.username}が退室しました",
        room_id=room_id,
        sender_id=1,
        sent_at=datetime.now(),
        signature_writer_name=system.username,
        message_type="system",  # Adjust as needed
        signature_avatar_url=avatar_url,  # Adjust as needed
        signature_trip="(emeth)",  # Adjust as needed
        signature_karma=str(777),  # Convert to string if necessary
        signature_profile=system.profile,
    )

    db.add(new_message)
    db.commit()
    return {"message": "Member removed from the room successfully"}


@router.put("/room/{room_id}/join_me", response_model=dict)
async def add_room_member(
    room_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = await request.json()
    # 部屋が存在するか確認
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if  room.room_type == "private":
        room_password=data.get("room_password"),
        if room.room_password != room_password :
            raise HTTPException(status_code=400, detail="Room Password incorect")

    # Check if the user is already a member of the room
    existing_member = (
        db.query(RoomMember)
        .filter(RoomMember.room_id == room_id, RoomMember.user_id == current_user.id)
        .first()
    )
    if existing_member:
        # すでに部屋にいる場合。退出処理がなんらかの原因でできていない
        #raise HTTPException(
        #    status_code=400, detail="You are already a member of this room"
        #)
        return {"message": "You have successfully joined the room"}

    # 部屋の定員を確認
    if len(room.room_members) >= room.max_capacity:
        raise HTTPException(status_code=400, detail="Room is already full")

    # 新しいメンバーを部屋に追加
    new_member = RoomMember(
        room_id=room_id, user_id=current_user.id, joined_at=func.now()
    )
    db.add(new_member)

    system = db.query(User).filter(User.id == 1).first()
    avatar_url = (
        db.query(AvatarList.avatar_url)
        .filter_by(avatar_id=current_user.avatar_id)
        .scalar()
    )

    new_message = Message(
        content=f"{current_user.username}が入室しました",
        room_id=room_id,
        sender_id=1,
        sent_at=datetime.now(),
        signature_writer_name=system.username,
        message_type="system",  # Adjust as needed
        signature_avatar_url=avatar_url,  # Adjust as needed
        signature_trip="(emeth)",  # Adjust as needed
        signature_karma=str(777),  # Convert to string if necessary
        signature_profile=system.profile,
    )

    db.add(new_message)
    db.commit()
    return {"message": "You have successfully joined the room"}


@router.put("/room/{room_id}/change_owner", response_model=Dict[str, Any])
async def change_room_owner(
    room_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = await request.json()
    new_owner_id = message_content = data.get("new_owner_id")
    # ユーザーが部屋のオーナーかどうかを確認
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if room.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not the owner of this room"
        )

    # 新しいオーナーが存在するかを確認
    new_owner = db.query(User).filter(User.id == new_owner_id).first()
    if not new_owner:
        raise HTTPException(status_code=404, detail="New owner not found")

    # 部屋のオーナーを変更
    room.owner_id = new_owner.id
    db.commit()

    return {"message": "Room owner changed successfully"}


@router.put("/room/{room_id}/close", response_model=Dict[str, Any])
async def close_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # ユーザーが部屋のオーナーかどうかを確認
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if room.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not the owner of this room"
        )

    # 部屋のステータスを「inactive」に変更
    room.status = "inactive"
    db.commit()

    return {"message": "Room closed successfully"}
