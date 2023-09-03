from fastapi import     Header,FastAPI,APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from chat_app.app.database.models import Message, Room, User,RoomMember,UserNGList
from chat_app.app.utils import create_db_engine_and_session, load_ng_words
from typing import Dict, Any
from fastapi import status
from pydantic import BaseModel
import requests
import jwt
from sqlalchemy.orm import joinedload
from typing import Dict, Any
from datetime import datetime, timedelta
import requests
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


def get_user_by_id(id: str, db: Session) -> User:
    user = db.query(User).filter(User.sub == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{sub} User not found")
    return user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def db_get_user_ng_list(user_id: int, db: Session):
    """
    指定したユーザーのNGリスト情報をデータベースから取得します。
    
    :param user_id: ユーザーのID
    :param db: データベースセッション
    :return: ユーザーのNGリスト情報
    """
    user_ng_list = db.query(UserNGList).filter(UserNGList.user_id == user_id).all()
    return user_ng_list

@router.get("/users/{user_id}/ng-list",  response_model=Dict[str, Any])
async def get_user_ng_list(
    user_id: int, db: Session = Depends(get_db)
):
    user_ng_list = db_get_user_ng_list(user_id, db)
    if not user_ng_list:
        raise HTTPException(status_code=404, detail="User NG List not found")
    return {1:user_ng_list}