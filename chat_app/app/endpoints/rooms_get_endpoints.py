from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from chat_app.app.database.models import Message, Room, User, RoomMember, AvatarList
from chat_app.app.utils import create_db_engine_and_session, load_ng_words
from typing import Dict, Any
from chat_app.app.utils import create_db_engine_and_session, get_public_key, escape_html
from sqlalchemy import func

# データベース関連の初期化
engine, SessionLocal, Base = create_db_engine_and_session()
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_active_room_member_count(room_id: int, db: Session):
    # 特定の部屋内でアクティブなユーザーの数を取得
    active_room_member_count = (
        db.query(RoomMember)
        .filter(RoomMember.room_id == room_id)
        .join(RoomMember.user)
        .count()
    )
    return active_room_member_count


@router.get("/rooms", response_model=Dict[str, Any])
def get_rooms(skip: int = 0, db: Session = Depends(get_db)):
    rooms = db.query(Room).offset(skip).all()
    response_data = {"rooms": []}

    for room in reversed(rooms):  # Display new messages at the top
        # Count active room members

        room_data = {
            "id": room.id,
            "room_type" : room.room_type ,
            "name": escape_html(room.name),
            "room_member_count": get_active_room_member_count(room.id, db),
            "label": escape_html(room.label),
            "max_capacity": room.max_capacity,
            "over_karma_limit": room.over_karma_limit,
            "under_karma_limit": room.under_karma_limit,
            "lux": room.lux,
            "status": room.status,
            "last_activity": room.last_activity,
            "owner_username": room.owner.username,
            "owner_avatar_url": (
                db.query(AvatarList.avatar_url)
                .filter(AvatarList.avatar_id == room.owner.avatar_id)
                .scalar()
            ),
            "room_members": [
                {
                    "username": escape_html(member.user.username),
                    "avatar_url": (
                        db.query(AvatarList.avatar_url)
                        .filter(AvatarList.avatar_id == member.user.avatar_id)
                        .scalar()
                    ),  # avatar_urlを取得し追加
                }
                for member in room.room_members
            ],
        }
        response_data["rooms"].append(room_data)

    return response_data
