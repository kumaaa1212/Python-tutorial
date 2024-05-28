from typing import Optional
from app.schemas.main import ItemBase, ItemStatus, ItemUpdate


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


def create(item_create: ItemBase):
    new_item = Item(
        len(items) + 1,
        item_create.name,
        item_create.price,
        item_create.description,
        ItemStatus.ON_SALE,
    )
    items.append(new_item)
    return new_item


def update(id: int, item_update: ItemUpdate):
    for item in items:
        if item.id == id:
            item.name = item.name if item_update.name is None else item_update.name
            item.price = item.price if item_update.price is None else item_update.price
            item.description = (
                item.description
                if item_update.description is None
                else item_update.description
            )
            item.status = (
                item.status if item_update.status is None else item_update.status
            )
            return item
    return None

# def update(id: int, item_update: ItemUpdate):
#     for item in items:
#         if item.id == id:
#             item.name = item_update.get("name", item.name)
#             item.price = item_update.get("price", item.price)
#             item.description = item_update.get("description", item.description)
#             item.status = item_update.get("status", item.status)
#             return item
#     return None

def delete(id: int):
    for i in range(len(items)):
        if items[i].id == id:
            delete_item = items.pop(i)
            return delete_item
    return None
