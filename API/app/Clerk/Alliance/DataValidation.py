# 数据校验模型
from pydantic import BaseModel
from typing import Optional
from fastapi import Query


class AddAlliance(BaseModel):
    alliance_name: str


class SearchAlliance(BaseModel):
    alliance_name: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10

    class Config:
        orm_mode = True


class UpdateAlliance(AddAlliance):
    id: int
    alliance_name: str = Query(None)