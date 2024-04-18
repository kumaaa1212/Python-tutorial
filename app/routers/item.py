from fastapi import APIRouter, Body
from app.services.cruds import item as item_cruds
from app.schemas import main as item_schemas

# 1番親の階層からの相対パスで記述する（違う方法ありそう）

# 共通設定はインスタンスを生成する時に、コンストラクタに設定することで使うことができる
router = APIRouter(prefix="/items", tags=["items"])


@router.get("")
async def find_all():
    return item_cruds.find_all()

@router.get("")
async def find_all():
    return item_cruds.find_all()

@router.get("/{id}")
async def find_by_id(id: int):
    return item_cruds.find_by_id(id)

# クエリパラメータを受け取る方法
# 使用する関数に引数を追加することで、クエリパラメータを受け取ることができる
# 最後に/をつけることで、エンドポイントが衝突しないようにしている
@router.get("/")
async def find_by_name(name: str):
    return item_cruds.find_by_name(name)

# 引数の型でスキーマクラスを使用することで、自動でバリデーションを行うことができる
@router.post("")
async def create(item_create=item_schemas.ItemBase):
    return item_cruds.create(item_create)

@router.put("/{id}")
async def update(id: int, item_update=Body()):
    return item_cruds.update(id, item_update)

@router.delete("/{id}")
async def delete(id: int):
    return item_cruds.delete(id)
