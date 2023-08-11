from fastapi import FastAPI
from fastapi import HTTPException
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello nddr"}

@app.get("/error400")
async def error_400():
    raise HTTPException(status_code=400, detail="Bad Request")

@app.get("/error401")
async def error_401():
    raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/error402")
async def error_402():
    raise HTTPException(status_code=402, detail="Payment Required")

@app.get("/error403")
async def error_403():
    raise HTTPException(status_code=403, detail="Forbidden")
