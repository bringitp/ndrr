from fastapi import FastAPI
from chat_app.app.endpoints.root_endpoints import router as root_router
from chat_app.app.endpoints.room_messages_post_endpoints import router as room_message_post_router
from chat_app.app.endpoints.room_messages_get_endpoints import router as room_message_get_router
from chat_app.app.endpoints.rooms_get_endpoints import router as rooms_get_router
from fastapi.staticfiles import StaticFiles
import os
app = FastAPI()

# main.pyのディレクトリパスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
# /chat_app/static/ を /main.pyのディレクトリ/static/ にマウント
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

# ルーターをアプリに追加
app.include_router(root_router)
app.include_router(rooms_get_router)
#app.include_router(rooms_post_router)
app.include_router(room_message_get_router)
app.include_router(room_message_post_router)


