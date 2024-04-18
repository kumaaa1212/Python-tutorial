from pydantic import BaseModel, Field
from typing import Optional

# BaseModelを継承してあげることで、スキーマクラスとして認識することができる
class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, examples=["item1"])
    price : int = Field(ge=0,examples=[1000])
    description: Optional[str] = Field(max_length=100,default=None, examples=["item1 description"])
    # description: Optional[str] = Field(None, max_length=100)