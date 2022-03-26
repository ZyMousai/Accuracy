# 数据校验模型
from pydantic import BaseModel
from typing import Optional
from fastapi import Query
from datetime import date


class Alarm(BaseModel):
    job_id: Optional[str] = None
    alarm_time: Optional[int] = None


class DelAlarm(BaseModel):
    job_id: Optional[str] = None


class SearchJob(BaseModel):
    job_id: Optional[str] = Query(None)
