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
from chat_app.app.database.models import Message, Room, User, RoomMember , AvatarList
from typing import Dict, Any
from datetime import datetime, timedelta
import requests
import jwt
from janome.tokenizer import Tokenizer
from collections import defaultdict
import html
import re
from chat_app.app.utils import create_db_engine_and_session, get_public_key, escape_html
from chat_app.app.auth_utils import (
    UserToken,
    LoginUser,
    validate_token,
    get_user_by_sub,
    skeltone_get_current_user,
    get_block_list,
)

import markdown


def markdown_to_html(markdown_text):
    html = markdown.markdown(markdown_text)
    return html


def replace_markdown_with_html(match):  # md形式
    markdown_text = match.group(1)
    html_output = markdown_to_html(markdown_text)
    return html_output


# データベース関連の初期化
engine, SessionLocal, Base = create_db_engine_and_session()
ng_words = load_ng_words()  # ng word 読み込み
# JWT関連の設定
public_key = get_public_key("https://ron-the-rocker.net/auth", "ndrr")

# Janomeのトークナイザーの初期化
t = Tokenizer()

# 前回の投稿時刻と投稿回数を記録するための辞書
user_post_data = defaultdict(lambda: {"last_post_time": None, "post_count": 0})
# 最大投稿回数
MAX_POST_COUNT = 5  # 5回までとする


# YouTubeのアドレスを検出して置き換える関数
def replace_youtube_links(match):
    video_id = match.group(5)
    iframe_tag = f'<iframe width="95%" src="https://www.youtube.com/embed/{video_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'
    return iframe_tag


def check_post_frequency_within_time(
    user_sub: str, db: Session, time_interval: timedelta, max_post_count: int
):
    now = datetime.now()
    user_data = user_post_data[user_sub]

    if user_data["last_post_time"]:
        elapsed_time = now - user_data["last_post_time"]
        if elapsed_time <= time_interval and user_data["post_count"] >= max_post_count:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests",
            )

        # Reset the post count if the elapsed time exceeds the interval
        if elapsed_time > time_interval:
            user_data["post_count"] = 0
    else:
        elapsed_time = time_interval + timedelta(
            seconds=1
        )  # Initialize elapsed_time with a value larger than time_interval

    user_data["last_post_time"] = now
    user_data["post_count"] += 1


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


def check_ng_words(message_content: str, ng_words: set) -> None:
    tokens = t.tokenize(message_content)
    if any(token.surface in ng_words for token in tokens):
        raise HTTPException(status_code=406, detail="NG words found in the message")


@router.post("/room/{room_id}/messages", response_model=Dict[str, Any])
async def create_room_message(
    room_id: int,
    request: Request,
    login_user: LoginUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    data = await request.json()
    message_content = data.get("message_content")
    if not message_content:
        raise HTTPException(status_code=422, detail="message_content is required")
    if len(message_content) > 350:
        raise HTTPException(status_code=406, detail="message_content is too long")

    # Check if the user is a member of the room
    room_member = (
        db.query(RoomMember).filter_by(room_id=room_id, user_id=login_user.id).first()
    )
    if not room_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this room",
        )

    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )

    if room.over_karma_limit < login_user.karma and room.over_karma_limit != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="More karma needed"
        )

    if room.under_karma_limit < login_user.karma and room.under_karma_limit != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="More real needed"
        )

    check_ng_words(message_content, ng_words)
    # Check post frequency within 180 seconds and 5 post count
    check_post_frequency_within_time(
        login_user.sub, db, timedelta(seconds=15), MAX_POST_COUNT
    )

    # Escape HTML characters in the message content
    sanitizing_content= escape_html(message_content)
    # 正規表現パターン
    youtube_url_regex = re.compile(
        r"^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/(watch\?v=)?([a-zA-Z0-9_-]{11})"
    )

    # YouTubeのアドレスを<iframe>タグに置き換える
    new_contents = youtube_url_regex.sub(replace_youtube_links, sanitizing_content)

    # Retrieve the current user's data
    current_user = db.query(User).filter_by(id=login_user.id).first()
    avatar_url = db.query(AvatarList.avatar_url).filter_by(avatar_id=current_user.avatar_id).scalar()
    # Populate the signature fields with the current user's data
    new_message = Message(
        content=new_contents ,
        room_id=room_id,
        sender_id=login_user.id,
        sent_at=datetime.now(),
        signature_writer_name=current_user.username,
        message_type ="public",  # Adjust as needed
        signature_avatar_url=avatar_url ,  # Adjust as needed
        signature_trip=current_user.trip,  # Adjust as needed
        signature_karma=str(current_user.karma),  # Convert to string if necessary
        signature_profile=current_user.profile,
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    response_data = {
        "room_id": room.id,
        "message_id": new_message.id,
        "content": new_message.content,
        "sent_at": new_message.sent_at,
        "sender": {"username": login_user.username, "karma": login_user.karma},
    }

    return response_data


@router.post("/room/{room_id}/private_messages", response_model=Dict[str, Any])
async def create_private_message(
        room_id: int,
        request: Request,
        login_user: LoginUser = Depends(get_current_user),
        db: Session = Depends(get_db),
        background_tasks: BackgroundTasks = BackgroundTasks()
    ):

    data = await request.json()
    message_content = data.get("message_content")
    receiver_id= data.get("receiver_id")
    if not message_content:
        raise HTTPException(status_code=422, detail="message_content is required")
    if len(message_content) > 350:
        raise HTTPException(status_code=406, detail="message_content is too long")

    # Check if the user is a member of the room
    room_member = (
        db.query(RoomMember).filter_by(room_id=room_id, user_id=login_user.id).first()
    )
    if not room_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this room",
        )

    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
        )

    if room.over_karma_limit < login_user.karma and room.over_karma_limit != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="More karma needed"
        )

    if room.under_karma_limit < login_user.karma and room.under_karma_limit != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="More real needed"
        )

    check_ng_words(message_content, ng_words)
    # Check post frequency within 180 seconds and 5 post count
    check_post_frequency_within_time(
        login_user.sub, db, timedelta(seconds=15), MAX_POST_COUNT
    )

    # Escape HTML characters in the message content
    sanitized_content = escape_html(message_content)

    # Retrieve the current user's data
    current_user = db.query(User).filter_by(id=login_user.id).first()
    avatar_url = db.query(AvatarList.avatar_url).filter_by(avatar_id=current_user.avatar_id).scalar()

    receiver_user = db.query(User).filter_by(id=receiver_id).first()
# ユーザーデータからユーザー名（名前）を抽出
    if receiver_user:
        receiver_name = receiver_user.username
    else:
    # ユーザーが存在しない場合、適切なエラー処理を行うか、デフォルトの値を設定します
        receiver_name = "Unknown User"

    # Populate the signature fields with the current user's data
    new_message = Message(
        content=sanitized_content,
        room_id=room_id,
        sender_id=login_user.id,
        receiver_id=receiver_id,
        sent_at=datetime.now(),
        signature_writer_name=current_user.username,
        signature_recipient_name =receiver_name,
        message_type ="private",  # Adjust as needed
        signature_avatar_url=avatar_url ,  # Adjust as needed
        signature_trip=current_user.trip,  # Adjust as needed
        signature_karma=str(current_user.karma),  # Convert to string if necessary
        signature_profile=current_user.profile,
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    response_data = {
        "room_id": room.id,
        "message_id": new_message.id,
        "content": new_message.content,
        "sent_at": new_message.sent_at,
        "sender": {"username": login_user.username, "karma": login_user.karma},
    }


