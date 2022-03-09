# 数据校验模型
from pydantic import BaseModel
from typing import Optional
from fastapi import Query



class SearchResult(BaseModel):
    name: str
    ip_address: str
    remark: str
    sucess_count: int
    fail_count: int

class ServerSearch(BaseModel):
    name: Optional[str]
    ip_address: Optional[str]
    page: Optional[int] = 1
    page_size: Optional[int] = 10

class AddServer(BaseModel):
    name: str = Query(...)
    ip_address: str = Query(...)
    password: Optional[str] = Query(...)
    remark: Optional[str] = Query(...)


class UpdateServer(BaseModel):
    id: int
    name: Optional[str] = Query(...)
    ip_address: Optional[str] = Query(...)
    password: Optional[str] = Query(...)
    # file: Optional[UploadFile] = File(...)
    remark: Optional[str] = Query(...)
