# 数据校验模型
from pydantic import BaseModel
from typing import Optional, List
from fastapi import Query


class SearchRole(BaseModel):
    role: Optional[str] = Query(None)
    creator: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10


class AddRole(BaseModel):
    role: Optional[str] = Query(...)
    creator: Optional[str] = Query(...)


class UpdateRole(BaseModel):
    id: int
    role: Optional[str] = Query(...)


class RoleAbout(BaseModel):
    role_id: int
    ids: Optional[List] = Query(...)
