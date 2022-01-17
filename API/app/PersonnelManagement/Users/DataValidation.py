# 数据校验模型
import datetime

from pydantic import BaseModel
from util.crypto import sha1_encode

from typing import Optional
from fastapi import Query


class AddUser(BaseModel):
    account: str
    password: str = sha1_encode("123456")
    name: str
    gender: bool
    birth: datetime.date
    entry_time: datetime.date
    phone: str
    address: str
    creator: Optional[str] = Query(...)


class UpdateUser(BaseModel):
    id: int
    name: Optional[str] = Query(None)
    gender: Optional[bool] = Query(None)
    birth: Optional[datetime.date] = Query(None)
    entry_time: Optional[datetime.date] = Query(None)
    phone: Optional[str] = Query(None)
    address: Optional[str] = Query(None)


class UpdatePassword(BaseModel):
    id: int
    password: Optional[str] = Query(..., min_length=6, max_length=16)
    update_password_time: Optional[datetime.datetime] = Query(datetime.datetime.now())


class SearchUser(BaseModel):
    name: Optional[str] = Query(None)
    gender: Optional[bool] = Query(None)
    creator: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10
