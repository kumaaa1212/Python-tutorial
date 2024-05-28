from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime

# BaseModelを継承してあげることで、スキーマクラスとして認識することができる


class ItemStatus(Enum):
    ON_SALE = "ON_SALE"
    SOLD_OUT = "SOLD_OUT"


class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, examples=["item1"])
    price: int = Field(ge=0, examples=[10000])
    description: Optional[str] = Field(
        max_length=100, default=None, examples=["item1 description"]
    )
    # description: Optional[str] = Field(None, max_length=100)


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, examples=["item1"])
    price: Optional[int] = Field(None, ge=0, examples=[10000])
    description: Optional[str] = Field(
        None, max_length=100, examples=["item1 description"]
    )
    status: Optional[ItemStatus] = Field(None, examples=[ItemStatus.ON_SALE])


class ItemResponse(BaseModel):
    id: int = Field(ge=1, examples=[1])
    name: str = Field(min_length=2, max_length=100, examples=["item1"])
    price: int = Field(ge=0, examples=[10000])
    description: Optional[str] = Field(
        None, max_length=100, examples=["item1 description"]
    )
    status: ItemStatus = Field(examples=[ItemStatus.ON_SALE])
    created_at: datetime
    updated_at: datetime
    # これらを追加して、スキーマを揃える

    model_config = ConfigDict(from_attributes=True)
    # このスキーマはormのオブジェクトを自動的に受け取り、適切なレスポンススキーマに変換するための設定を行っている
