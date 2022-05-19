# 数据校验模型
from pydantic import BaseModel

from typing import Optional
from fastapi import Query


class OffersUnionSearch(BaseModel):
    union_name:Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    union_system_id:Optional[int]
    page: Optional[int] = 1
    page_size: Optional[int] = 10


class AddOffersUnion(BaseModel):
    union_name: str
    union_url: str
    union_system_id: int


class UpdateOffersUnion(BaseModel):
    id: int
    union_name: Optional[str]
    union_url: Optional[str]
    union_system_id: Optional[int]
