from fastapi import APIRouter, Path, Query, HTTPException, Depends
from starlette import status
from app.services.cruds import item as item_cruds
from app.schemas.main import ItemBase, ItemUpdate, ItemResponse
from typing import Optional
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session

# テストの際に実際のデータベースを使わずにすむ
DbDepend = Annotated[Session, Depends(get_db)]

# 共通設定はインスタンスを生成する時に、コンストラクタに設定することで使うことができる
router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
async def find_all(db: DbDepend):
    return item_cruds.find_all(db)


@router.get("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def find_by_id(db: DbDepend, id: int = Path(gt=0)):
    fund_id = item_cruds.find_by_id(db, id)
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
async def create(db: DbDepend, item_create: ItemBase):
    return item_cruds.create(db, item_create)


@router.put("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def update(db: DbDepend, item_update: ItemUpdate, id: int = Path(gt=0)):
    updated_item = item_cruds.update(db, id, item_update)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@router.delete("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def delete(db: DbDepend, id: int = Path(gt=0)):
    deleted_item = item_cruds.delete(db, id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_item
