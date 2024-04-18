from typing import Optional
from enum import Enum
from app.schemas import main as item_schemas

class ItemStatus(Enum):
    ON_SALE = "ON_SALE"
    SOLD_OUT = "SOLD_OUT"


class Item:
    def __init__(
        self,
        id: int,
        name: str,
        price: int,
        description: Optional[str],
        status: ItemStatus,
    ):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.status = status


items = [
    Item(1, "item1", 100, "item1 description", ItemStatus.ON_SALE),
    Item(2, "item2", 200, "item2 description", ItemStatus.SOLD_OUT),
    Item(3, "item3", 300, "item3 description", ItemStatus.ON_SALE),
]


def find_all():
    return items


def find_by_id(id: int):
    for item in items:
        if item.id == id:
            return item
    return None


def find_by_name(name: str):
    filterd_items = []
    for item in items:
        if name in item.name:
            filterd_items.append(item)
    return filterd_items

# getはbodyの要素を取得している。
# getを使わない理由は？なぜgetを使うのか？
def create(item_create: item_schemas.ItemBase):
    new_item = Item(
        len(items) + 1,
        item_create.name,
        item_create.price,
        item_create.description,
        ItemStatus.ON_SALE,
    )
    items.append(new_item)
    return new_item

def update(id: int, item_update):
    for item in items:
        if item.id == id:
            item.name = item_update.get("name", item.name)
            item.price = item_update.get("price", item.price)
            item.description = item_update.get("description", item.description)
            item.status = item_update.get("status", item.status)
            return item
    return None

def delete(id: int):
    for i in range(len(items)):
        if items[i].id == id:
            delete_item = items.pop(i)
            return delete_item
    return None