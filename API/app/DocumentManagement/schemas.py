from datetime import datetime
from typing import List
from pydantic import BaseModel, validator


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
