from datetime import datetime
from fastapi import Query
from pydantic import BaseModel, validator
from typing import Optional, List


class DocumentManagementModel(BaseModel):
    id: int
    filename: str
    filesize: str
    # user_name:str
    created_time: str

    # permission_name: str

    @validator("created_time", pre=True)
    def parse_birthdate(cls, value):
        if isinstance(value, datetime):
            data = value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            data = value
        return data

    class Config:
        orm_mode = True


class CreateDocumentManagement(BaseModel):
    filename: str
    filesize: str
    user_id: str
    created_time: datetime


class SearchDocumentManagement(BaseModel):
    page: int = 1
    page_size: int = 10
    filename: Optional[str] = None
    user_name: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    department_id: Optional[str] = None


class UpdateDocumentManagement(BaseModel):
    id: int
    department_id: Optional[str] = None
