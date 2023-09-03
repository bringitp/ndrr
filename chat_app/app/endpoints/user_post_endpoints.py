from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from chat_app.app.database.models import Message, Room, User,RoomMember
from chat_app.app.utils import create_db_engine_and_session, load_ng_words
from typing import Dict, Any

# データベース関連の初期化
engine, SessionLocal, Base = create_db_engine_and_session()
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/rooms", response_model=Dict[str, Any])
def get_rooms(skip: int = 0, db: Session = Depends(get_db)):
    rooms = db.query(Room).offset(skip).all()
    response_data = {
        "rooms": []
    }

    for room in reversed(rooms):  # Display new messages at the top
        room_data = {
            "id": room.id,
            "name": room.name,
            "label": room.label,
            "owner_id": room.owner_id,
            "max_capacity": room.max_capacity,
            "over_karma_limit": room.over_karma_limit,
            "under_karma_limit": room.under_karma_limit,
            "lux": room.lux,
            "status": room.status,
            "last_activity": room.last_activity,
            "owner": room.owner,
            "room_members": [
                {
                    "id": member.user.id,
                    "username": member.user.username,
                }
                for member in room.room_members
            ],
        }
        response_data["rooms"].append(room_data)

    return response_data


    return rooms
