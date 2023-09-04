from fastapi import FastAPI, Depends, Header, HTTPException, status, APIRouter, Request, BackgroundTasks
from sqlalchemy.orm import Session
from chat_app.app.utils import create_db_engine_and_session, load_ng_words
from chat_app.app.database.models import Message, Room, User,RoomMember,PrivateMessage
from typing import Dict, Any
from datetime import datetime, timedelta
import requests
import jwt
from janome.tokenizer import Tokenizer
from collections import defaultdict
import html
import re

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

@router.post("/room/{room_id}", response_model=Dict[str, Any])
async def create_room_message(
    room_id: int, 
    request: Request,
    login_user: LoginUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
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

@router.put("/room/{room_id}/remove_member", response_model=dict)
async def remove_room_member(
    room_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    data = await request.json()
    member_id = message_content = data.get("member_id")

    # ユーザーが部屋のオーナーかどうかを確認
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if room.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this room")

    # メンバーを部屋から削除
    member = db.query(RoomMember).filter(RoomMember.room_id == room_id, RoomMember.user_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found in the room")

    db.delete(member)
    db.commit()
    return {"message": "Member removed from the room successfully"}

@router.put("/room/{room_id}/change_owner", response_model=Dict[str, Any])
async def change_room_owner(
    room_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    data = await request.json()
    new_owner_id = message_content = data.get("new_owner_id")
    # ユーザーが部屋のオーナーかどうかを確認
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if room.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this room")

    # 新しいオーナーが存在するかを確認
    new_owner = db.query(User).filter(User.id == new_owner_id).first()
    if not new_owner:
        raise HTTPException(status_code=404, detail="New owner not found")

    # 部屋のオーナーを変更
    room.owner_id = new_owner.id
    db.commit()

    return {"message": "Room owner changed successfully"}

@router.put("/room/{room_id}/close", response_model=Dict[str, Any])
async def close_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ユーザーが部屋のオーナーかどうかを確認
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if room.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this room")

    # 部屋のステータスを「inactive」に変更
    room.status = "inactive"
    db.commit()

    return {"message": "Room closed successfully"}


app.include_router(router)

