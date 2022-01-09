# 数据校验模型
from pydantic import BaseModel
from util.crypto import sha1_encode

from typing import Optional
from fastapi import Query


class AddUser(BaseModel):
    account: str
    password: str = sha1_encode("123456")
    name: str
    gender: bool
    birth: str
    entry_time: str
    phone: str
    address: str


class UpdateUser(BaseModel):
    id: int
    name: Optional[str] = Query(None)
    gender: Optional[bool] = Query(None)
    birth: Optional[str] = Query(None)
    entry_time: Optional[str] = Query(None)
    phone: Optional[str] = Query(None)
    address: Optional[str] = Query(None)


class UpdatePassword(BaseModel):
    id: int
    password: str = Query(..., min_length=6, max_length=16)
