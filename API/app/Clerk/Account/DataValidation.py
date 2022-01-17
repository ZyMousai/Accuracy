# 数据校验模型
from pydantic import BaseModel
from typing import Optional
from fastapi import Query


class AddAccount(BaseModel):
    card_id: int
    account_id: int
    alliance_id: int
    task: str
    commission: float
    consume: float
    user: Optional[str] = Query(None)
    secondary_consumption: int


class UpdateAccount(BaseModel):
    id: int
    card_id: Optional[int] = Query(None)
    account_id: Optional[int] = Query(None)
    alliance_id: Optional[int] = Query(None)
    task: Optional[str] = Query(None)
    commission: Optional[float] = Query(None)
    consume: Optional[float] = Query(None)
    user: Optional[str] = Query(None)
    secondary_consumption: Optional[int] = Query(None)


class SearchAccount(BaseModel):
    card_id: Optional[int] = Query(None)
    account_id: Optional[int] = Query(None)
    alliance_id: Optional[int] = Query(None)
    task: Optional[str] = Query(None)
    user: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10
