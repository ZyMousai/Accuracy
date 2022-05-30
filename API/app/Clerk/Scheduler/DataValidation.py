# 数据校验模型
from pydantic import BaseModel
from typing import Optional
from fastapi import Query


class Alarm(BaseModel):
    # job_name: Optional[str] = None
    # alarm_time: Optional[int] = None
    key: Optional[str] = None


class DelAlarm(BaseModel):
    job_name: Optional[str] = None


class SearchJob(BaseModel):
    job_name: Optional[str] = Query(None)


class DisplaySearchJob(BaseModel):
    job_name: Optional[str] = Query(None)
    start_create_time: Optional[str] = Query(None)
    end_create_time: Optional[str] = Query(None)
    alarm: Optional[int] = Query(None)
    state: Optional[int] = Query(None)
    at: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10


class DisplayAddJob(BaseModel):
    job_name: str
    interval: int
    alarm: int
    at: str


class DisplayUpdateJob(BaseModel):
    id: int
    job_name: Optional[str] = Query(None)
    interval: Optional[int] = Query(None)
    alarm: Optional[int] = Query(None)
    at: Optional[str] = Query(None)


class RebootMachine(BaseModel):
    job_name: str

