# 数据校验模型
from pydantic import BaseModel
from typing import Optional
from fastapi import Query


class AddCard(BaseModel):
    alliance_name: str


class UpdateCard(BaseModel):
    id: int
    alliance_name: Optional[str] = Query(None)


class SearchCard(BaseModel):
    alliance_name: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10
