# 数据校验模型
from pydantic import BaseModel
from typing import Optional
from fastapi import Query


class AddAccount(BaseModel):
    account_name: str


class SearchAccount(BaseModel):
    account_name: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10

    class Config:
        orm_mode = True


class UpdateAccount(AddAccount):
    id: int
    account_name: str = Query(None)



