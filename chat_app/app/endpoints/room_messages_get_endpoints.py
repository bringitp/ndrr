from fastapi import (
    FastAPI,
    Depends,
    Header,
    HTTPException,
    status,
    APIRouter,
)
from sqlalchemy.orm import Session, aliased

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
import functools
import time
from chat_app.app.utils import (
    create_db_engine_and_session
    ,get_public_key
)
def escape_html(text):
    return html.escape(text, quote=True)

app = FastAPI()

# データベース関連の初期化
engine, SessionLocal, Base = create_db_engine_and_session()
public_key = get_public_key("https://ron-the-rocker.net/auth","ndrr")

# Janomeのトークナイザーの初期化
router = APIRouter()
class UserToken:
    sub: str

class LoginUser(UserToken):
    id: int
    karma: int
    username: str
    avatar: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# キャッシュデコレータを定義
def lru_cache_with_headers(maxsize=None, typed=False, cache_timeout=5):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # ヘッダー情報をキーにする
            header_key = kwargs.get("Authorization")
            if header_key is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bearer token missing")
            
            key = (header_key, args, frozenset(kwargs.items()))
            if key in cache and time.time() - cache[key]["time"] < cache_timeout:
                return cache[key]["value"]
            result = func(*args, **kwargs)
            cache[key] = {"value": result, "time": time.time()}
            return result
        return wrapper
    return decorator

# ブロックリストを取得する関数
def get_block_list(user_id: int, db: Session):
    block_list = db.query(UserNGList.blocked_user_id).filter(UserNGList.user_id == user_id).all()
    return [item[0] for item in block_list]


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

# キャッシュデコレータを使用して関数をデコレート
# 24.78 [#
#  Requests per second:    24.68 [#/sec] (mean)
@lru_cache_with_headers(maxsize=None, typed=False, cache_timeout=15)
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
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Invalid token {token_string}")

    user = get_user_by_sub(sub, db)
    return user

@router.get("/room/{room_id}/messages", response_model=Dict[str, Any])
async def get_room_messages(
    room_id: int, skip: int = 0, limit: int = 50,
    login_user: LoginUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    room = db.query(Room).get(room_id)
    # Check if the user is a member of the room
    if not db.query(RoomMember).filter_by(room_id=room_id, user_id=login_user.id).first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this room")

    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    if room.over_karma_limit < login_user.karma and room.over_karma_limit != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="More karma needed")

    if room.under_karma_limit < login_user.karma and room.under_karma_limit != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="More real needed")

    # メンバー情報を一括で取得
    room_members = (
        db.query(RoomMember)
        .filter(RoomMember.room_id == room_id)
        .all()
    )

# Eager Loadingを使用してユーザー情報とアバター情報を一括で取得
#    user_ids = [room_member.user_id for room_member in room_members]
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
        avatar_id_and_url = next((avatar_url for user_id, avatar_url in user_avatar_urls if user_id == user.id), None)
    # ブロック済みユーザーかどうかを確認
        blocked = user.id in block_list  # block_listに含まれているかどうかを確認
        if blocked:
            blocked_user_ids.add(user.id)
        vital_member_info.append({
             "user_id": user.id,
             "username": user.username,
             "avatar_url":  avatar_id_and_url,
             "blocked": bool(blocked),
             "ami"    :  bool(user.id==login_user.id),
         })
    # vital_member_info から user_id と avatar_url の対応を作成
    user_id_to_avatar_url = {member['user_id']: member['avatar_url'] for member in vital_member_info}
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
        "room_members": vital_member_info,# 部屋の現在のメンバー
        "messages": [],
        "version" : "0.02",
    }

    # UserとAvatarListのEager Loadingを追加
    # private message 取得
    private_messages = (
        db.query(PrivateMessage)
        .options(
            joinedload(PrivateMessage.sender).load_only('avatar_id'),
            joinedload(PrivateMessage.receiver).load_only('avatar_id')
        )
        .filter(
            (
                (PrivateMessage.receiver_id == login_user.id ) |
                (PrivateMessage.sender_id == login_user.id )
            ) 
            & (PrivateMessage.room_id == room_id)
            & (~PrivateMessage.sender_id.in_(block_list))  # 送信者がブロックリストに含まれていないことを確認
        )
        .order_by(PrivateMessage.sent_at.desc())
        .limit(min(limit, 30))
        .all()
    )

    # normal message 取得
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
    # private messageのIDと normal massage のIDをかぶらないようにする
    for message in private_messages:
        message.id += 1000

    all_messages = sorted(
        private_messages + normal_messages,
        key=lambda message: message.sent_at,
        reverse=True
    )

    for message in all_messages:
        is_private = isinstance(message, PrivateMessage)
        sender_id = message.sender_id
        sender_avatar_id_and_url = next((avatar_url for user_id, avatar_url in user_avatar_urls if user_id == sender_id), None)

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
                    #"profile": escape_html(sender.profile),
                    "sender_id": message.sender_id if is_private else None,
                    "receiver_id": message.receiver_id if is_private else None,
                    "receiver_username": "all",
                },
                "is_private": is_private
            }
    
            if is_private:
                receiver_user = db.query(User).filter(User.id == message.receiver_id).first()
                if receiver_user:
                    message_data["sender"]["receiver_username"] = escape_html(receiver_user.username)
    
            response_data["messages"].append(message_data)

    return response_data