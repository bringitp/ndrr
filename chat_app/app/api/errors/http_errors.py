# chat_app/app/api/errors/http_errors.py

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

class HTTPExceptionHandler:
    def __init__(self, app):
        self.app = app
        self.register_handlers()

    def register_handlers(self):
        self.app.add_exception_handler(HTTPException, self.http_exception_handler)

    async def http_exception_handler(self, request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )