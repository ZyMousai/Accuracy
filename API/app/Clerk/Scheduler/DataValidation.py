# 数据校验模型
from pydantic import BaseModel
from typing import Optional
from fastapi import Query


class Alarm(BaseModel):
    # job_name: Optional[str] = None
    # alarm_time: Optional[int] = None
    key: Optional[int] = None


class DelAlarm(BaseModel):
    job_id: Optional[str] = None


class SearchJob(BaseModel):
    job_id: Optional[str] = Query(None)


class DisplaySearchJob(BaseModel):
    job_name: Optional[str] = Query(None)
    start_create_time: Optional[str] = Query(None)
    end_create_time: Optional[str] = Query(None)
    alarm: Optional[int] = Query(None)
    state: Optional[int] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10

