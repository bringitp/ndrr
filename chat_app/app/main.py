from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.brotli import BrotliMiddleware
from chat_app.app.endpoints.root_endpoints import router as root_router
from chat_app.app.endpoints.room_messages_post_endpoints import router as room_message_post_router
from chat_app.app.endpoints.room_messages_get_endpoints import router as room_message_get_router
from chat_app.app.endpoints.rooms_get_endpoints import router as rooms_get_router
from chat_app.app.endpoints.users_endpoints import router as users_endpoints
from chat_app.app.endpoints.room_endpoints import router as room_endpoints
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Brotli 圧縮ミドルウェアを追加
app.add_middleware(BrotliMiddleware, minimum_size=1000)
# CORS設定を行う
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ここに許可したいオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# main.pyのディレクトリパスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
# /chat_app/static/ を /main.pyのディレクトリ/static/ にマウント
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

# ルーターをアプリに追加
app.include_router(root_router)
app.include_router(rooms_get_router)
app.include_router(users_endpoints)
app.include_router(room_message_get_router)
app.include_router(room_message_post_router)
app.include_router(room_endpoints)

