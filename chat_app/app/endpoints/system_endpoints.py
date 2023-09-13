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
from chat_app.app.database.models import Message, Room, User, RoomMember, AvatarList
from typing import Dict, Any
from datetime import datetime, timedelta
import requests
import jwt
from janome.tokenizer import Tokenizer
from collections import defaultdict
import html
import re
from sqlalchemy.sql import func
from chat_app.app.utils import create_db_engine_and_session, get_public_key, escape_html
from chat_app.app.auth_utils import (
    UserToken,
    LoginUser,
    validate_token,
    get_user_by_sub,
    skeltone_get_current_user,
    get_block_list,
)

# データベース関連の初期化
engine, SessionLocal, Base = create_db_engine_and_session()
ng_words = load_ng_words()  # ng word 読み込み
# JWT関連の設定
public_key = get_public_key("https://ron-the-rocker.net/auth", "ndrr")

# Janomeのトークナイザーの初期化

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


@router.get("/system/icons", response_model=Dict[str, Any])
async def create_room(
    request: Request,
    #current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    icons = db.query(AvatarList).all()
    icon_dict = {icon.avatar_id: icon.avatar_url for icon in icons}
    return icon_dict

