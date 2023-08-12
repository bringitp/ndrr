from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from chat_app.app.utils import create_db_engine_and_session
from chat_app.app.database.models import Message,User
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import selectinload
from typing import List
import sys
import configparser
app = FastAPI()
engine, SessionLocal, Base = create_db_engine_and_session()

@app.get("/")
async def read_root():
    return {"message": "Hello nddr"}

# メッセージとユーザー情報を取得するエンドポイント
@app.get("/rooms/{room_id}/messages")
async def get_room_messages(room_id: int, skip: int = 0, limit: int = 10):
    db = SessionLocal()
    
    # メッセージとユーザー情報を取得
    messages = db.query(Message).filter(Message.room_id == room_id).offset(skip).limit(limit).all()
    response_data = []
    for message in messages:
        sender = db.query(User).filter(User.id == message.sender_id).first()
        message_data = {
            "id": message.id,
            "room_id": message.room_id,
            "content": message.content,
            "sent_at": message.sent_at,
            "sender": {
                "username": sender.username,
                "avatar": sender.avatar
            }
        }
        response_data.append(message_data)
    
    return response_data


@app.get("/error400")
async def error_400():
    raise HTTPException(status_code=400, detail="Bad Request")

@app.get("/error401")
async def error_401():
    raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/error402")
async def error_402():
    raise HTTPException(status_code=402, detail="Payment Required")

@app.get("/error403")
async def error_403():
    raise HTTPException(status_code=403, detail="Forbidden")
