from fastapi import FastAPI, Depends, Header, HTTPException, status, APIRouter, Request, BackgroundTasks
from sqlalchemy.orm import Session
from chat_app.app.utils import create_db_engine_and_session, load_ng_words
from chat_app.app.database.models import Message, Room, User,RoomMember,AvatarList
from typing import Dict, Any
from datetime import datetime, timedelta
import requests
import jwt
from janome.tokenizer import Tokenizer
from collections import defaultdict
import html
from datetime import datetime

from sqlalchemy.orm import aliased


def escape_html(text):
    return html.escape(text, quote=True)

app = FastAPI()

# イベントハンドラの定義
def on_startup():
    # アプリケーション起動時の処理
    pass

def on_shutdown():
    # アプリケーション終了時の処理
    pass

app.add_event_handler("startup", on_startup)
app.add_event_handler("shutdown", on_shutdown)

# データベース関連の初期化
engine, SessionLocal, Base = create_db_engine_and_session()
ng_words = load_ng_words()  # ng word 読み込み

# JWT関連の設定
keycloak_url = "https://ron-the-rocker.net/auth"
realm = "ndrr"
jwks_url = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/certs"
response = requests.get(jwks_url)
jwks_data = response.json()
public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwks_data['keys'][0])

# Janomeのトークナイザーの初期化
t = Tokenizer()

router = APIRouter()

class UserToken:
    sub: str

class LoginUser(UserToken):
    id: int
    karma: int
    username: str
    avatar: str

# 前回の投稿時刻を記録するための辞書
last_post_times = defaultdict(lambda: None)

# 最大投稿回数
MAX_POST_COUNT = 3

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(Authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    if not Authorization:
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
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token payload")
    return sub

def get_user_by_sub(sub: str, db: Session) -> User:
    user = db.query(User).filter(User.sub == sub).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{sub} User not found")
    return user

def check_post_frequency_within_15_seconds(user_id: int, db: Session) -> None:
    now = datetime.now()
    recent_messages = (
        db.query(Message)
        .filter(Message.sender_id == user_id)
        .order_by(Message.sent_at.desc())
        .limit(3)
        .all()
    )
    post_count_within_15_seconds = sum(1 for message in recent_messages if (now - message.sent_at) <= timedelta(seconds=15))
    if post_count_within_15_seconds >= 3:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests within 15 seconds")

def check_ng_words(message_content: str, ng_words: set) -> None:
    tokens = t.tokenize(message_content)
    if any(token.surface in ng_words for token in tokens):
        raise HTTPException(status_code=406, detail="NG words found in the message")

@router.get("/room/{room_id}/messages", response_model=Dict[str, Any])
async def get_room_messages(
    room_id: int, skip: int = 0, limit: int = 50,
    login_user: LoginUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if the user is a member of the room
    room_member = (
        db.query(RoomMember)
        .filter_by(room_id=room_id, user_id=login_user.id)
        .first()
    )
    if not room_member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this room")

    room = db.query(Room).get(room_id)  # Room.idで直接取得可能
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    if room.over_karma_limit < login_user.karma and room.over_karma_limit != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="More karma needed")

    if room.under_karma_limit < login_user.karma and room.under_karma_limit != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="More real needed")

    sender_alias = aliased(User)
    avatar_alias = aliased(AvatarList)

    messages = (
        db.query(Message, sender_alias, avatar_alias)
        .join(sender_alias, Message.sender_id == sender_alias.id)
        .outerjoin(avatar_alias, sender_alias.avatar_id == avatar_alias.avatar_id)
        .filter(Message.room_id == room_id)
        .order_by(Message.id.desc())
        .offset(skip)
        .limit(min(limit, 30))
        .all()
    )

    room_owner = (
        db.query(User.username)
        .filter(User.id == room.owner_id)
        .first()
    )


    count = db.query(RoomMember).filter(RoomMember.room_id == room_id).count()

    response_data = {
        "room": {
            "room_id": room.id,
            "room_label": room.label,
            "room_name": room.name,
            "room_count": count,
            "room_owner_id": room.owner_id,
            "room_login_user_name": login_user.username,
            "room_owner_name": room_owner.username,
            "room_max_capacity": room.max_capacity,
            "room_restricted_karma_over_limit": room.over_karma_limit,
            "room_restricted_karma_under_limit": room.under_karma_limit,
            "room_lux": room.lux,
        },
        "messages": []
    }

    sender_ids = [message.sender_id for message, _, _ in messages]
    senders = (
        db.query(User)
        .filter(User.id.in_(sender_ids))
        .all()
    )

    avatar_ids = [sender.avatar_id for sender in senders if sender.avatar_id]
    avatars = (
        db.query(AvatarList)
        .filter(AvatarList.avatar_id.in_(avatar_ids))
        .all()
    )

    for message, sender, avatar in messages:
        avatar_url = None
        if avatar:
            avatar_url = avatar.avatar_url

        message_data = {
            "id": message.id,
            "room_id": message.room_id,
            "content": message.content,
            "toxicity": message.toxicity,
            "sentiment": message.sentiment,
            "fluence": message.fluence,
            "sent_at": message.sent_at.strftime("%y-%m-%d %H:%M:%S"),
            "sender": {
                "username": escape_html(sender.username),
                "avatar_url": avatar_url,
                "trip": escape_html(sender.trip),
                "karma": sender.karma,
                "privilege": sender.privilege,
                "lastlogin_at": sender.lastlogin_at.strftime("%m-%d %H:%M"),  # 西暦下2桁の年に変換
                "penalty_points": sender.penalty_points,
                "profile": escape_html(sender.profile)
            },
        }
        response_data["messages"].append(message_data)

    return response_data