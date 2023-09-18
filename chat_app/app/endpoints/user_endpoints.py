from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session, joinedload
from chat_app.app.database.models import Message, Room, User, RoomMember, UserNGList,AvatarList
from chat_app.app.utils import create_db_engine_and_session, load_ng_words
from datetime import datetime, timedelta
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Any, Optional
import jwt
import requests
from janome.tokenizer import Tokenizer
from collections import defaultdict
import html
from chat_app.app.utils import (
    create_db_engine_and_session
    ,get_public_key
    ,escape_html
)
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

public_key = get_public_key("https://ron-the-rocker.net/auth","ndrr")
# Janomeのトークナイザーの初期化
t = Tokenizer()
router = APIRouter()
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
    return skeltone_get_current_user(Authorization,db,public_key)

def get_user_by_id(id: str, db: Session) -> User:
    user = db.query(User).filter(User.sub == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{sub} User not found")
    return user

def db_get_user_ng_list(user_id: int, db: Session):
    user_ng_list = db.query(UserNGList).filter(UserNGList.user_id == user_id).all()
    return user_ng_list

@router.get("/user/profile", response_model=Dict[str, Any])
async def get_user_profile(
    current_user: LoginUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    user_id = current_user.id  # Use the user ID from the current user's JWT token
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    avatar_url = (
            db.query(AvatarList.avatar_url)
            .filter_by(avatar_id=current_user.avatar_id)
            .scalar()
            )

    # LoginUserモデルから必要なフィールドを抽出して辞書に格納
    user_data = {
        "id": current_user.id,
        "username": current_user.username,
        "trip": current_user.trip,
        "profile": current_user.profile,
        "life": current_user.life,
        "created_at": current_user.created_at,
        "profile": current_user.profile,
        "penalty_points": current_user.penalty_points,
        "sub": current_user.sub,
        # 他の必要なフィールドを追加
    }

    response = dict()
    response["user_profile"] = user_data  # user_dataを"user_profile"というキーで追加
    response["avatar_url"] = avatar_url

    return response  # JSONとしてuser_dataとavatar_urlを含むレスポンスを返す

class UserUpdate(BaseModel):
    username: Optional[str] = None
    profile: Optional[str] = None
    trip: Optional[str] = None
    life: Optional[int] = None
    karma: Optional[float] = None

@router.put("/user/profile", response_model=Dict[str, Any])
async def update_user_profile(
    user_update_data: UserUpdate,
    current_user: User = Depends(get_current_user),  # ログインユーザーを取得
    db: Session = Depends(get_db)
):
    # ログインユーザーの ID とユーザ情報更新データを使用して、データベースからユーザを取得
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ユーザ情報を更新
    for field, value in user_update_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    # データベースに変更をコミット
    db.commit()
    db.refresh(user)

    # 更新後のユーザ情報を返す
    updated_user_data = {
        "username": user.username,
        "profile": user.profile,
        "trip": user.trip
        # 必要に応じて他のフィールドを追加
    }

    return {"message": "User profile updated successfully", "user_profile": updated_user_data}

@router.get("/user/ng-list", response_model=List[Any])
async def get_user_ng_list(
    current_user: LoginUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    user_id = current_user.id  # Use the user ID from the current user's JWT token
    user_ng_list = db_get_user_ng_list(user_id, db)
    if not user_ng_list:
        raise HTTPException(status_code=404, detail="User NG List not found")
    return user_ng_list

@router.post("/user/ng-list",  response_model=Dict[Any,Any])
async def create_user_ng_item(
    request: Request,
    login_user: LoginUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    data = await request.json()
    blocked_user_id = data.get("blocked_user_id")
    user_id = login_user.id  # ユーザーのJWTトークンからIDを取得
    # 既存のNGリストに同じ組み合わせが存在しないかチェック
    existing_ng_item = db.query(UserNGList).filter_by(user_id=user_id, blocked_user_id=blocked_user_id).first()
    if existing_ng_item:
        raise HTTPException(status_code=400, detail="この組み合わせは既に存在します。")

    new_ng_item = UserNGList(user_id=user_id, blocked_user_id=blocked_user_id)
    db.add(new_ng_item)
    db.commit()
    db.refresh(new_ng_item)
 
    return {"success":"ok"}

@router.delete("/user/ng-list", response_model=Dict[Any,Any])
async def delete_user_ng_item(
    request: Request, current_user: LoginUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    data = await request.json()
    blocked_user_id = data.get("blocked_user_id")
    user_id = current_user.id  # ユーザーのJWTトークンからIDを取得
    ng_item = db.query(UserNGList).filter(UserNGList.blocked_user_id == blocked_user_id , UserNGList.user_id == user_id).first()
    if not ng_item:
        raise HTTPException(status_code=404, detail="NG Item not found")
    
    # NG アイテムを削除する処理を書く
    db.delete(ng_item)
    db.commit()
    
    return {"success":"ok"}