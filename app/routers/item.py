from fastapi import APIRouter, Path, Query, HTTPException, Depends
from starlette import status
from app.services.cruds import item as item_cruds
from app.services.auth import main as auth_cruds
from app.schemas.main import ItemBase, ItemUpdate, ItemResponse, TokenData
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session

# テストの際に実際のデータベースを使わずにすむ
DbDepend = Annotated[Session, Depends(get_db)]

# 共通設定はインスタンスを生成する時に、コンストラクタに設定することで使うことができる
router = APIRouter(prefix="/items", tags=["items"])


UserDepend = Annotated[TokenData, Depends(auth_cruds.get_current_user)]


@router.get("", response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
async def find_all(db: DbDepend):
    return item_cruds.find_all(db)


@router.get("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def find_by_id(db: DbDepend, user: UserDepend, id: int = Path(gt=0)):
    fund_id = item_cruds.find_by_id(db, id, user.user_id)
    if not fund_id:
        raise HTTPException(status_code=404, detail="Item not found")
    return fund_id


@router.get("/", response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
async def find_by_name(db: DbDepend, name: str = Query(min_length=2, max_length=100)):
    return item_cruds.find_by_name(db, name)


# db: DbDependにすることで、データベースへのセッションをcreate関数に渡すことができる
@router.post(
    "/create", response_model=ItemResponse, status_code=status.HTTP_201_CREATED
)
async def create(db: DbDepend, user: UserDepend, item_create: ItemBase):
    print(user.user_id)
    return item_cruds.create(db, item_create, user.user_id)


@router.put("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def update(db: DbDepend, user: UserDepend, item_update: ItemUpdate, id: int = Path(gt=0)):
    updated_item = item_cruds.update(db, id, item_update, user.user_id)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@router.delete("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def delete(db: DbDepend,  user: UserDepend, id: int = Path(gt=0)):
    deleted_item = item_cruds.delete(db, id, user.user_id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_item
