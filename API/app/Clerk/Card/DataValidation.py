# 数据校验模型
from pydantic import BaseModel
from typing import Optional
from fastapi import Query
from datetime import date


class AddCard(BaseModel):
    card_number: Optional[str] = None
    face_value: Optional[float] = None
    valid_period: Optional[str] = None
    cvv: Optional[str] = None
    card_status: Optional[int] = None
    name: Optional[str] = None
    platform: Optional[str] = None
    note: Optional[str] = None
    create_time: Optional[date] = None
    # retain: Optional[int] = 0
    retain: Optional[int] = None
    card_name: Optional[str] = None


class UpdateCard(AddCard):
    id: int


class SearchCard(AddCard):
    page: Optional[int] = 1
    page_size: Optional[int] = 10

    class Config:
        orm_mode = True


class AddAccount(BaseModel):
    # account_name: str
    uid: str


class SearchAccount(BaseModel):
    # account_name: Optional[str] = Query(None)
    uid: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10

    class Config:
        orm_mode = True


class UpdateAccount(AddAccount):
    id: int
    # account_name: str = Query(None)
    uid: str = Query(None)


# class AddAlliance(BaseModel):
#     alliance_name: str
#
#
# class SearchAlliance(BaseModel):
#     alliance_name: Optional[str] = Query(None)
#     page: Optional[int] = 1
#     page_size: Optional[int] = 10
#
#     class Config:
#         orm_mode = True
#
#
# class UpdateAlliance(AddAlliance):
#     id: int
#     alliance_name: str = Query(None)


class AddTask(BaseModel):
    card_id: int
    account_id: int
    # alliance_id: int
    task: str
    note: Optional[str] = None
    commission: float
    consume: float
    user: Optional[str] = Query(None)
    secondary_consumption: int


class UpdateTask(BaseModel):
    id: int
    card_id: Optional[int] = Query(None)
    account_id: Optional[int] = Query(None)
    # alliance_id: Optional[int] = Query(None)
    task: Optional[str] = Query(None)
    note: Optional[str] = Query(None)
    commission: Optional[float] = Query(None)
    consume: Optional[float] = Query(None)
    user: Optional[str] = Query(None)
    secondary_consumption: Optional[int] = Query(None)


class Statistics(BaseModel):
    uid: Optional[str] = Query(None)
    start_time: Optional[str] = Query(None)
    end_time: Optional[str] = Query(None)


class SearchTask(BaseModel):
    card_id: Optional[int] = Query(None)
    account_id: Optional[int] = Query(None)
    # alliance_id: Optional[int] = Query(None)
    task: Optional[str] = Query(None)
    user: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10


class Export(BaseModel):
    start_time: Optional[str] = Query(None)
    end_time: Optional[str] = Query(None)