from fastapi import FastAPI
from chat_app.app.endpoints.root_endpoints import router as root_router
from chat_app.app.endpoints.room_endpoints import router as room_router

app = FastAPI()

# ルーターをアプリに追加
app.include_router(root_router)
app.include_router(room_router)


