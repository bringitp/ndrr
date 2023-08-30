from fastapi import FastAPI, Depends, Header, HTTPException, status, APIRouter, Request, BackgroundTasks
from sqlalchemy.orm import Session
from chat_app.app.utils import create_db_engine_and_session, load_ng_words
from chat_app.app.database.models import Message, Room, User,RoomMember
from typing import Dict, Any
from datetime import datetime, timedelta
import requests
import jwt
from janome.tokenizer import Tokenizer
from collections import defaultdict
import html
def escape_html(text):
    return html.escape(text, quote=True)

import markdown

def markdown_to_html(markdown_text):
    html = markdown.markdown(markdown_text)
    return html

def replace_markdown_with_html(match): # md形式
    markdown_text = match.group(1)
    html_output = markdown_to_html(markdown_text)
    return html_output



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

# 前回の投稿時刻と投稿回数を記録するための辞書
user_post_data = defaultdict(lambda: {"last_post_time": None, "post_count": 0})

# 最大投稿回数
MAX_POST_COUNT = 5  # 5回までとする

def check_post_frequency_within_time(user_sub: str, db: Session, time_interval: timedelta, max_post_count: int):
    now = datetime.now()
    user_data = user_post_data[user_sub]

    if user_data["last_post_time"]:
        elapsed_time = now - user_data["last_post_time"]
        if elapsed_time <= time_interval and user_data["post_count"] >= max_post_count:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests")

        # Reset the post count if the elapsed time exceeds the interval
        if elapsed_time > time_interval:
            user_data["post_count"] = 0
    else:
        elapsed_time = time_interval + timedelta(seconds=1)  # Initialize elapsed_time with a value larger than time_interval

    user_data["last_post_time"] = now
    user_data["post_count"] += 1

    
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def check_ng_words(message_content: str, ng_words: set) -> None:
    tokens = t.tokenize(message_content)
    if any(token.surface in ng_words for token in tokens):
        raise HTTPException(status_code=406, detail="NG words found in the message")

@router.post("/rooms/{room_id}/messages", response_model=Dict[str, Any])
async def create_room_message(
    room_id: int, 
    request: Request,
    login_user: LoginUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):

    data = await request.json()
    message_content = data.get("message_content")
    if not message_content:
        raise HTTPException(status_code=422, detail="message_content is required")
    if len(message_content) > 350:
        raise HTTPException(status_code=406, detail="message_content is too long")

    # Check if the user is a member of the room
    room_member = db.query(RoomMember).filter_by(room_id=room_id, user_id=login_user.id).first()
    if not room_member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this room")

    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    if room.over_karma_limit < login_user.karma and room.over_karma_limit != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="More karma needed")

    if room.under_karma_limit < login_user.karma and room.under_karma_limit != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="More real needed")
        

    check_ng_words(message_content, ng_words)
    # Check post frequency within 180 seconds and 5 post count
    check_post_frequency_within_time(login_user.sub, db, timedelta(seconds=15), MAX_POST_COUNT)

    new_message = Message(content=message_content, room_id=room_id, sender_id=login_user.id, sent_at=datetime.now())
 
    # htmlをエスケープする
    new_message = escape_html(new_message)
 
    pattern = r"```(.*?)```"  # 正規表現パターンで```...```に囲まれた部分を抽出
    output_text = re.sub(pattern, replace_markdown_with_html, input_text, flags=re.DOTALL)
    output_text = output_text.replace(r"```(.*?)```", replacement_text)

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
            "karma": login_user.karma
        },
    }

    return response_data

app.include_router(router)
