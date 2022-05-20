# 数据校验模型
from pydantic import BaseModel

from typing import Optional, List, Dict
from fastapi import Query


class OffersAccountSearch(BaseModel):
    union_name: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    offers_account: Optional[str]
    status: Optional[int]
    page: Optional[int] = 1
    page_size: Optional[int] = 10


class AddOffersAccount(BaseModel):
    union_id: int
    offers_account: str
    offers_pwd: str
    offers_api_key: Optional[str]
    options: Optional[List[Dict]] = Query([])
    status: int = Query(1)
    ip_info: Optional[Dict] = Query({"nation": "US", "state": ""})


class UpdateOffersAccount(BaseModel):
    id: int
    union_id: Optional[int]
    offers_account: Optional[str]
    offers_pwd: Optional[str]
    offers_api_key: Optional[str]
    options: Optional[List[Dict]]
    status: Optional[int]
    ip_info: Optional[Dict]
