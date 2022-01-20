from typing import Optional

from fastapi import Query
from pydantic import BaseModel


# 数据模型
class AddCampaignMapping(BaseModel):
    m_id: str
    m_name: str
    s_id: str
    s_name: str

    class Config:
        orm_mode = True


class SearchCampaignMapping(BaseModel):
    m_id: Optional[int] = Query(None)
    m_name: Optional[str] = Query(None)
    s_id: Optional[int] = Query(None)
    s_name: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10
