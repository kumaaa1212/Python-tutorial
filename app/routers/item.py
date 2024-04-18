from fastapi import APIRouter, Path, Query, HTTPException
from starlette import status
# starletteはpythonの基盤となるフレームワーク
from app.services.cruds import item as item_cruds
from app.schemas.main import ItemBase, ItemUpdate, ItemResponse
from typing import Optional

# 1番親の階層からの相対パスで記述する（違う方法ありそう）

# 共通設定はインスタンスを生成する時に、コンストラクタに設定することで使うことができる
router = APIRouter(prefix="/items", tags=["items"])

# fastapiは基本的に200を返す。エラーを返す場合は、HTTPExceptionを使う
# createの場合もHTTP_200_OKを返す。これを変更したい時に、status_code=status.HTTP_201_CREATEDを使う
# 200でも明示的に書く
@router.get("", response_model=list[ItemResponse], status_code=status.HTTP_200_OK)
async def find_all():
    return item_cruds.find_all()

@router.get("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def find_by_id(id: int = Path(gt=0)):
    fund_id = item_cruds.find_by_id(id)
    if not fund_id:
        raise HTTPException(status_code=404, detail="Item not found")
    return fund_id

# クエリパラメータを受け取る方法
# 使用する関数に引数を追加することで、クエリパラメータを受け取ることができる
# 最後に/をつけることで、エンドポイントが衝突しないようにしている
# リクエストbodyを取得したい時は、Body()もしくはスキーマクラスを使用する
@router.get("/", response_model=Optional[ItemResponse], status_code=status.HTTP_200_OK)
async def find_by_name(name: str = Query(min_length=2, max_length=100)):
    return item_cruds.find_by_name(name)


# 引数の型でスキーマクラスを使用することで、自動でバリデーションを行うことができる
@router.post("/create", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create(item_create: ItemBase):
    return item_cruds.create(item_create)


# async def create(item_create=ItemBase):
#     return item_cruds.create(item_create)
# =にしてしまうと、中身を取得する系になってしまう


# 対象がない場合があるから、optionalを使う
@router.put("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def update(item_update: ItemUpdate, id: int = Path(gt=0)):
    updated_item = item_cruds.update(id, item_update)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")


# 対象がない場合があるから、optionalを使う
@router.delete("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def delete(id: int = Path(gt=0)):
    deleted_item = item_cruds.delete(id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_item
# Optional[ItemResponse]にしていたが、エラーを吐かせるようにしたのでけした
