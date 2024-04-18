from fastapi import FastAPI
from app.routers import item
# 同じディレクトリでないからこのように書いている
# crudsの中のitemモジュール

# FastAPIはクラスのため、ここでインスタンスを作成している
app = FastAPI()
app.include_router(item.router)
