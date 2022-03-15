# 数据校验模型
from pydantic import BaseModel

from typing import Optional
from fastapi import Query


class SearchAccount(BaseModel):
    account: Optional[str] = Query(None)
    platform: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10


class AddAccount(BaseModel):
    account: str
    platform: str
    password: str
    remark: Optional[str] = Query("")


class UpdateAccount(BaseModel):
    id: int
    account: Optional[str] = Query(None)
    platform: Optional[str] = Query(None)
    password: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)
