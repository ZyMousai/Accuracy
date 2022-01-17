# 数据校验模型
from pydantic import BaseModel
from typing import Optional
from fastapi import Query


class AddDepartmentUserMapping(BaseModel):
    department_id: int
    user_id: int


class UpdateDepartmentUserMapping(BaseModel):
    id: int
    department_id: Optional[int] = Query(None)
    user_id: Optional[int] = Query(None)


class SearchDepartmentUserMapping(BaseModel):
    department_id: Optional[int] = Query(None)
    user_id: Optional[int] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10
