# 数据校验模型
from pydantic import BaseModel
from typing import Optional
from fastapi import Query


class AddDepartmentRoleMapping(BaseModel):
    department_id: int
    role_id: int


class UpdateDepartmentRoleMapping(BaseModel):
    id: int
    department_id: Optional[int] = Query(None)
    role_id: Optional[int] = Query(None)


class SearchDepartmentRoleMapping(BaseModel):
    department_id: Optional[int] = Query(None)
    role_id: Optional[int] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10
