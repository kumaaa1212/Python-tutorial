from fastapi import APIRouter, Path, Query, HTTPException
from starlette import status
from app.services.cruds import item as item_cruds
from app.schemas.main import ItemBase, ItemUpdate, ItemResponse
from typing import Optional


# 共通設定はインスタンスを生成する時に、コンストラクタに設定することで使うことができる
router = APIRouter(prefix="/items", tags=["items"])
@router.get("", response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
async def find_all():
    return item_cruds.find_all()

@router.get("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def find_by_id(id: int = Path(gt=0)):
    fund_id = item_cruds.find_by_id(id)
    if not fund_id:
        raise HTTPException(status_code=404, detail="Item not found")
    return fund_id

@router.get("/", response_model=Optional[ItemResponse], status_code=status.HTTP_200_OK)
async def find_by_name(name: str = Query(min_length=2, max_length=100)):
    return item_cruds.find_by_name(name)


@router.post("/create", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create(item_create: ItemBase):
    return item_cruds.create(item_create)

@router.put("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def update(item_update: ItemUpdate, id: int = Path(gt=0)):
    updated_item = item_cruds.update(id, item_update)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def delete(id: int = Path(gt=0)):
    deleted_item = item_cruds.delete(id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_item
