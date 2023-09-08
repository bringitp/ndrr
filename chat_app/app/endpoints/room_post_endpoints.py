from fastapi import (
    FastAPI, Depends, Header, HTTPException, status, APIRouter, Request, BackgroundTasks
)
from sqlalchemy.orm import Session
from chat_app.app.utils import (
    create_db_engine_and_session, load_ng_words, create_db_engine_and_session, get_public_key  ,escape_html
)
from chat_app.app.database.models import (
    Message, Room, User, RoomMember
)
from typing import Dict, Any
from datetime import datetime, timedelta
import jwt
from janome.tokenizer import Tokenizer
import markdown
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

def replace_markdown_with_html(match): # md形式
    markdown_text = match.group(1)
    html_output = markdown_to_html(markdown_text)
    return html_output

# データベース関連の初期化
engine, SessionLocal, Base = create_db_engine_and_session()
ng_words = load_ng_words()  # ng word 読み込み

public_key = get_public_key("https://ron-the-rocker.net/auth","ndrr")

# Janomeのトークナイザーの初期化
t = Tokenizer()
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(Authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    return skeltone_get_current_user(Authorization,db,public_key)


def check_ng_words(message_content: str, ng_words: set) -> None:
    tokens = t.tokenize(message_content)
    if any(token.surface in ng_words for token in tokens):
        raise HTTPException(status_code=406, detail="NG words found in the message")

@router.post("/room/{room_id}", response_model=Dict[str, Any])
async def create_room_message(
    room_id: int, 
    request: Request,
    login_user: LoginUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    data = await request.json()
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    # ユーザーがメンバーでない場合、403エラーを返す
    room_member = db.query(RoomMember).filter_by(room_id=room_id, user_id=login_user.id).first()
    if not room_member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this room")

    # ルームを取得
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    # ログインユーザーがルームの管理者でない場合、403エラーを返す
    if room.owner_id != login_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this room")

    # 新しい部屋名を設定
    room.name = message_content = data.get("room_name")
    room.max_capacity  = data.get("max_capacity")
    room.label = data.get("room_label")
    # データベースに変更をコミット
    db.commit()

    response_data = {
        "message": "Room name changed successfully"
    }

    return response_data

app.include_router(router)

