# 数据校验模型
from pydantic import BaseModel
from typing import Optional, List
from fastapi import Query
from datetime import date


class AddCard(BaseModel):
    card_number: Optional[str] = None
    face_value: Optional[float] = None
    valid_period: Optional[str] = None
    cvv: Optional[str] = None
    card_status: Optional[bool] = None
    name: Optional[str] = None
    platform: Optional[str] = None
    note: Optional[str] = None
    create_time: Optional[date] = None
    retain: Optional[int] = 0
    card_name: Optional[str] = None


class UpdateCard(AddCard):
    id: int


class SearchCard(AddCard):
    page: Optional[int] = 1
    page_size: Optional[int] = 10

    class Config:
        orm_mode = True
