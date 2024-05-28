from typing import Optional
from app.schemas.main import ItemBase, ItemStatus, ItemUpdate
from sqlalchemy.orm import Session
from models import Item

# class Item:
#     def __init__(
#         self,
#         id: int,
#         name: str,
#         price: int,
#         description: Optional[str],
#         status: ItemStatus,
#     ):
#         self.id = id
#         self.name = name
#         self.price = price
#         self.description = description
#         self.status = status


# items = [
#     Item(1, "item1", 100, "item1 description", ItemStatus.ON_SALE),
#     Item(2, "item2", 200, "item2 description", ItemStatus.SOLD_OUT),
#     Item(3, "item3", 300, "item3 description", ItemStatus.ON_SALE),
# ]


# queryに検索したいモデルを指定することで、データベースからデータを取得することができる
def find_all(db: Session):
    return db.query(Item).all()


# 最初に見つかったデータを返す
def find_by_id(db: Session, id: int):
    return db.query(Item).filter(Item.id == id).first()


def find_by_name(db: Session, name: str):
    return db.query(Item).filter(Item.name.like(f"%{name}%")).all()


# model_dump()はスキーマの内容を辞書型に変換するメソッド
# **を二つつけることであんパックすることができる
def create(db: Session, item_create: ItemBase):
    new_item = Item(**item_create.model_dump())
    db.add(new_item)
    db.commit()
    return new_item


def update(db: Session, id: int, item_update: ItemUpdate):
    item = find_by_id(db, id)
    if not item:
        return None
    item.name = item.name if item_update.name is None else item_update.name
    item.price = item.price if item_update.price is None else item_update.price
    item.description = (
        item.description if item_update.description is None else item_update.description
    )
    item.status = item.status if item_update.status is None else item_update.status
    db.add(item)
    db.commit()
    return item


# def update(id: int, item_update: ItemUpdate):
#     for item in items:
#         if item.id == id:
#             item.name = item_update.get("name", item.name)
#             item.price = item_update.get("price", item.price)
#             item.description = item_update.get("description", item.description)
#             item.status = item_update.get("status", item.status)
#             return item
#     return None


def delete(db: Session, id: int):
    item = find_by_id(db, id)
    if not item:
        return None
    db.delete(item)
    db.commit()
    return item