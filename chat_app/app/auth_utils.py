# auth_utils.py
import jwt
from fastapi import HTTPException, status,Depends
from chat_app.app.database.models import User,UserNGList
from sqlalchemy.orm import Session
import cachetools
from datetime import datetime
# キャッシュの設定（10秒のTTLキャッシュ）
token_cache = cachetools.TTLCache(maxsize=1000, ttl=180)

class UserToken:
    sub: str

class LoginUser(UserToken):
    id:     int
    karma: int
    username: str
    avatar: str

def validate_token(token_string: str, public_key: str) -> str:
    # キャッシュからトークンの検証結果を取得
    cached_sub = token_cache.get(token_string)
    if cached_sub:
        return cached_sub

    options = {"verify_signature": True, "verify_aud": False, "exp": True}
    payload = jwt.decode(token_string, public_key, algorithms=["RS256"], options=options)
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token payload")

    # トークンを検証し、有効期限を確認
    exp_timestamp = payload.get("exp")
    if exp_timestamp:
        current_timestamp = datetime.timestamp(datetime.now())
        if current_timestamp >= exp_timestamp:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

    # キャッシュにトークン検証結果を保存
    token_cache[token_string] = sub

    return sub

def get_user_by_sub(sub: str, db: Session) -> User:
    user = db.query(User).filter(User.sub == sub).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{sub} User not found")
    return user

# ブロックリストを取得する関数
def get_block_list(user_id: int, db: Session):
    block_list = db.query(UserNGList.blocked_user_id).filter(UserNGList.user_id == user_id).all()
    return [item[0] for item in block_list]

def skeltone_get_current_user(Authorization: str, db: Session,public_key) -> User:
    if not Authorization:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bearer token missing")
    try:
        bearer, token_string = Authorization.split()
        if bearer != "Bearer":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Bearer token format")
        sub = validate_token(token_string, public_key)  # public_key の値は適切な値に置き換える

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid token")

    user = get_user_by_sub(sub, db) 
    return user