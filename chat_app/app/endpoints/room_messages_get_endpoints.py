from fastapi import (
    FastAPI,
    Depends,
    Header,
    HTTPException,
    status,
    APIRouter,
)
from sqlalchemy.orm import Session, aliased
from chat_app.app.utils import (
    create_db_engine_and_session,
    load_ng_words
)
from chat_app.app.database.models import (
    Message,
    Room,
    User,
    RoomMember,
    AvatarList,
    PrivateMessage,
    UserNGList
)
from sqlalchemy.orm import joinedload
from typing import Dict, Any
from datetime import datetime, timedelta
import requests
import jwt
from janome.tokenizer import Tokenizer
from collections import defaultdict
import html

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


# ブロックリストを取得する関数
def get_block_list(user_id: int, db: Session):
    block_list = db.query(UserNGList.blocked_user_id).filter(UserNGList.user_id == user_id).all()
    return [item[0] for item in block_list]

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
    room_member = db.query(RoomMember).filter_by(room_id=room_id, user_id=login_user.id).first()
    if not room_member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this room")

    room = db.query(Room).get(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    if room.over_karma_limit < login_user.karma and room.over_karma_limit != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="More karma needed")

    if room.under_karma_limit < login_user.karma and room.under_karma_limit != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="More real needed")

    room_owner = db.query(User.username).filter(User.id == room.owner_id).first()
    member_count = db.query(RoomMember).filter(RoomMember.room_id == room_id).count()

    response_data = {
        "room": {
            "room_id": room.id,
            "room_label": room.label,
            "room_name": room.name,
            "room_member_count": member_count,
            "room_owner_id": room.owner_id,
            "room_login_user_name": login_user.username,
            "room_login_user_id": login_user.id,
            "room_owner_name": room_owner.username,
            "room_max_capacity": room.max_capacity,
            "room_restricted_karma_over_limit": room.over_karma_limit,
            "room_restricted_karma_under_limit": room.under_karma_limit,
            "room_lux": room.lux,
        },
        "messages": []
    }

    block_list = get_block_list(login_user.id, db)

    # UserとAvatarListのEager Loadingを追加
    private_messages = (
        db.query(PrivateMessage)
        .options(
            joinedload(PrivateMessage.sender).load_only('avatar_id'),
            joinedload(PrivateMessage.receiver).load_only('avatar_id')
        )
        .filter(
            (
                ((PrivateMessage.receiver_id == login_user.id) & (PrivateMessage.sender_id == room_member.user_id)) |
                ((PrivateMessage.sender_id == login_user.id) & (PrivateMessage.receiver_id == room_member.user_id))
            ) &
            (~PrivateMessage.sender_id.in_(block_list))  # 送信者がブロックリストに含まれていないことを確認
        )
        .order_by(PrivateMessage.sent_at.desc())
        .limit(min(limit, 30))
        .all()
    )

    for message in private_messages:
        message.id += 10000000000

    normal_messages = (
        db.query(Message)
        .options(
             joinedload(Message.sender).load_only('avatar_id')
        )
        .filter(
             (Message.room_id == room_id) &
             (~Message.sender_id.in_(block_list))
        )
        .order_by(Message.sent_at.desc())
        .offset(skip)
        .limit(min(limit, 30))
        .all()
    )

    all_messages = sorted(
        private_messages + normal_messages,
        key=lambda message: message.sent_at,
        reverse=True
    )

    for message in all_messages:
        is_private = isinstance(message, PrivateMessage)
        sender = db.query(User).filter(User.id == message.sender_id).first()
        if sender:
            avatar_id = sender.avatar_id
            avatar_url = (
                db.query(AvatarList.avatar_url)
                .filter(AvatarList.avatar_id == avatar_id)
                .scalar()
            )

        message_data = {
            "id": message.id,
            "room_id": message.room_id,
            "content": message.content,
            "toxicity": message.toxicity,
            "sentiment": message.sentiment,
            "fluence": message.fluence,
            "sent_at": message.sent_at.strftime("%y-%m-%d %H:%M:%S"),
            "short_sent_at": message.sent_at.strftime("%H:%M"),
            "sender": {
                "username": escape_html(sender.username),
                "user_id": sender.id,
                "avatar_url": avatar_url,
                "trip": escape_html(sender.trip),
                "karma": sender.karma,
                "privilege": sender.privilege,
                "lastlogin_at": sender.lastlogin_at.strftime("%m-%d %H:%M"),
                "penalty_points": sender.penalty_points,
                "profile": escape_html(sender.profile),
                "sender_id": message.sender_id if is_private else None,
                "receiver_id": message.receiver_id if is_private else None,
                "sender_username": None,
            },
            "is_private": is_private
        }

        if is_private:
            receiver_user = db.query(User).filter(User.id == message.receiver_id).first()
            if receiver_user:
                message_data["sender"]["sender_username"] = escape_html(receiver_user.username)

        response_data["messages"].append(message_data)

    return response_data
