# 数据校验模型
from pydantic import BaseModel
from typing import Optional
from fastapi import Query
from enum import Enum


class UpdateOffers(BaseModel):
    id: int
    remark: Optional[str] = Query(...)


class PayFilter(str, Enum):
    lt = "<"
    le = "<="
    eq = "=="
    ge = ">="
    gt = ">"
    ne = "!="


class SearchOffers(BaseModel):
    union_id: Optional[int] = Query(None)
    account_id: Optional[int] = Query(None)
    offers_name: Optional[str] = Query(None)
    pay: Optional[int] = Query(None)
    pay_filter: Optional[PayFilter]
    country: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10
