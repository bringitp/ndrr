from fastapi import FastAPI, Depends, Header, HTTPException, status, APIRouter, Request
from sqlalchemy.orm import Session
from chat_app.app.utils import create_db_engine_and_session
from chat_app.app.database.models import Message, Room, User
from typing import Dict, Any
from datetime import datetime
import requests
import jwt
from janome.tokenizer import Tokenizer
import logging
# ログ設定
logging.basicConfig(level=logging.INFO)  # ログレベルを設定

app = FastAPI()
engine, SessionLocal, Base = create_db_engine_and_session()

keycloak_url = "https://ron-the-rocker.net/auth"
realm = "ndrr"
jwks_url = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/certs"
response = requests.get(jwks_url)
jwks_data = response.json()
public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwks_data['keys'][1])

router = APIRouter()

class UserToken:
    sub: str

class LoginUser(UserToken):
    id: int
    karma: int
    username: str
    avatar: str

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(Authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    if Authorization is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bearer token missing")

    try:
        bearer, token_string = Authorization.split()
        if bearer != "Bearer":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Bearer token format")

        sub = validate_token(token_string)

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid token")

    user = get_user_by_sub(sub, db)
    return user

def validate_token(token_string: str) -> str:
    options = {"verify_signature": True, "verify_aud": False, "exp": True}
    payload = jwt.decode(token_string, public_key, algorithms=["RS256"], options=options)
    sub: str = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token payload")
    return sub

def get_user_by_sub(sub: str, db: Session) -> User:
    user = db.query(User).filter(User.sub == sub).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@router.get("/rooms/{room_id}/messages", response_model=Dict[str, Any])
async def get_room_messages(
    room_id: int, skip: int = 0, limit: int = 10,
    login_user: LoginUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    if room.over_karma_limit < login_user.karma and room.over_karma_limit != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="More karma needed")

    if room.under_karma_limit < login_user.karma and room.under_karma_limit != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="More real needed")

    messages = (
        db.query(Message)
        .filter(Message.room_id == room_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    response_data = {
        "room": {
            "room_id": room.id,
            "room_label": room.label,
            "room_name": room.name,
            "room_owner_id": room.owner_id,
            "room_max_capacity": room.max_capacity,
            "room_restricted_karma_over_limit": room.over_karma_limit,
            "room_restricted_karma_under_limit": room.under_karma_limit,
            "room_lux": room.lux,
        },
        "messages": []
    }

    for message in messages:
        sender = db.query(User).filter(User.id == message.sender_id).first()
        message_data = {
            "id": message.id,
            "room_id": message.room_id,
            "content": message.content,
            "toxicity": message.toxicity,
            "sentiment": message.sentiment,
            "fluence": message.fluence,            
            "sent_at": message.sent_at,
            "sender": {
                "username": sender.username,
                "avatar": sender.avatar,
                "karma": sender.karma,
                "profile": sender.profile
            },
        }
        response_data["messages"].append(message_data)

    return response_data

@router.post("/rooms/{room_id}/messages", response_model=Dict[str, Any])
async def create_room_message(
    room_id: int, 
    request: Request,
    login_user: LoginUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):



    data = await request.json()
    message_content = data.get("message_content")
    if message_content is None:
        raise HTTPException(status_code=422, detail="message_content is required")
    if message_content is length(message_content) > 255:
        raise HTTPException(status_code=406, detail="message_content is too long")
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    if room.over_karma_limit < login_user.karma and room.over_karma_limit != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="More karma needed")

    if room.under_karma_limit < login_user.karma and room.under_karma_limit != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="More real needed")

    t = Tokenizer()
    tokens = t.tokenize(message_content)

    for token in tokens:
        logging.info(f"Surface: {token.surface}, Part of Speech: {token.part_of_speech}")  # ログを記録

    new_message = Message(content=message_content, room_id=room_id, sender_id=login_user.id, toxicity=1000, sent_at=datetime.now())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    response_data = {
        "room_id": room.id,
        "message_id": new_message.id,
        "content": new_message.content,
        "sent_at": new_message.sent_at,
        "sender": {
            "username": login_user.username,
            "avatar": login_user.avatar,
            "karma": login_user.karma,
            "profile": login_user.profile
        },
    }

    return response_data

app.include_router(router)
