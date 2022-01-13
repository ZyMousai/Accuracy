# 数据校验模型
from pydantic import BaseModel
from typing import Optional
from fastapi import Query


class AddDepartments(BaseModel):
    department: str
    creator: Optional[str] = Query(None)


class UpdateDepartment(BaseModel):
    id: int
    department: Optional[str] = Query(None)


class SearchDepartment(BaseModel):
    department: Optional[str] = Query(None)
    creator: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10
