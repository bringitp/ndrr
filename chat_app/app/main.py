from fastapi import FastAPI, HTTPException, Depends, Header,status
from sqlalchemy.orm import Session
from chat_app.app.utils import create_db_engine_and_session
from chat_app.app.database.models import Message, User,Room
from typing import List,Dict,Any
from jose import jwt
import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
import requests
import os

app = FastAPI()
engine, SessionLocal, Base = create_db_engine_and_session()
keycloak_url = "https://ron-the-rocker.net/auth"
realm = "ndrr"

class UserToken:
    sub: str

class LoginUser(UserToken):
    id: int
    karma: int
    username: str
    avatar: str    

def get_current_user(Authorization: str = Header(None)) -> User:
    if Authorization is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bearer token missing")

    try:
        bearer, token_string = Authorization.split()
        if bearer != "Bearer":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Bearer token format")

        options = {"verify_signature": True, "verify_aud": False, "exp": True}
        jwks_url = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/certs"
        response = requests.get(jwks_url)
        jwks_data = response.json()
        token_bytes = token_string.encode('utf-8')
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwks_data['keys'][0])
        payload = jwt.decode(token_bytes, public_key, algorithms=["RS256"], options=options)
        sub: str = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token payload")

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    db = SessionLocal()
    user = db.query(User).filter(User.sub == sub).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@app.get("/rooms/{room_id}/messages", response_model=Dict[str, Any])
async def get_room_messages(
    room_id: int, skip: int = 0, limit: int = 10,
    login_user: LoginUser = Depends(get_current_user)
):

    db = SessionLocal()
    room = db.query(Room).filter(Room.id == room_id).offset(skip).limit(limit).first()
    response_data = {
        "room" : {
            "room_id": room.id,
            "room_name": room.name,
            "room_owner_id": room.owner_id,
            "room_max_capacity" : room.max_capacity ,
            "room_restricted_level_by_karma" : room.restricted_level_by_karma 
        } ,
        "messages" : []
    }

    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    if room.restricted_level_by_karma  > login_user.karma:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="More karma needed")

    messages = (
        db.query(Message)
        .filter(Message.room_id == room_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    for message in messages:
        sender = db.query(User).filter(User.id == message.sender_id).first()
        message_data = {
            "id": message.id,
            "room_id": message.room_id,
            "content": message.content,
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
