from pydantic import BaseModel
from typing import Optional
from enum import Enum


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
