from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# class DocumentManagementModel(BaseModel):
#     id: int
#     filename: str
#     file_size: str
#     # user_name:str
#     created_time: str
#
#     # permission_name: str
#
#     @validator("created_time", pre=True)
#     def parse_birth_date(cls, value):
#         if isinstance(value, datetime):
#             data = value.strftime("%Y-%m-%d %H:%M:%S")
#         else:
#             data = value
#         return data
#
#     class Config:
#         orm_mode = True


class CreateDocumentManagement(BaseModel):
    filename: str
    filesize: str
    user_id: str
    created_time: datetime


class SearchDocumentManagement(BaseModel):
    page: int = 1
    page_size: int = 10
    filename: Optional[str]
    user_name: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
