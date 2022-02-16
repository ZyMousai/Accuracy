from fastapi import Query
from pydantic import BaseModel
from enum import Enum
from typing import Optional


class PlatformEnum(str, Enum):
    ios_iphone = "iphone"
    android_phone = "android"
    ios_ipad = "ipad"
    windows_desktop = "desktop"


class CountryEnum(str, Enum):
    JP = "jp"
    US = "us"
    TW = "tw"
    GB = "gb"
    DE = "de"


class SearchTrackLink(BaseModel):
    platform: PlatformEnum
    country: CountryEnum
    url: str


class AddTrackAlliance(BaseModel):
    name: str
    url: str


class UpdateTrackAlliance(BaseModel):
    id: int
    name: Optional[str] = Query(None)
    url: Optional[str] = Query(None)


class AddTrackUrl(BaseModel):
    track_url: str
    alliance_id: int


class SearchTrackAlliance(BaseModel):
    name_or_url: Optional[str] = Query(None)
    track_url: Optional[str] = Query(None)
    page: Optional[int] = 1
    page_size: Optional[int] = 10
