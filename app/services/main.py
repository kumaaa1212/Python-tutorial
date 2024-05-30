from fastapi import FastAPI
from app.routers import item, auth
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    # allow_credentials=True,
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request, call_next):
    # apiエンドポイントの実際のリクエストが実行される。responseが実行されたものが返ってくる
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(item.router)
app.include_router(auth.router)
