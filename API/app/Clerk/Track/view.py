# Track 视图
import datetime
import requests

from typing import Optional, List
from app.Clerk.Track.DataValidation import SearchTrackLink
from sql_models.db_config import db_session
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

track_router = APIRouter(
    prefix="/track/v1",
    responses={404: {"description": "Not found"}},
    tags=["Track"])

# 登录url
MOBRAND_LOGOIN_URL = "https://api.mobrand.net/login"
# 抓取url
MOBRAND_TRACK_URL = "https://api.offertest.net/offertest/console"

# token
TOKEN = dict()

USER_INFO = {
    "user_id": "4NgG9ZnvQKq3NiSQ7WtvAQ",
    "login_info": {
        "email": "wuhanyouyu@gmail.com",
        "password": "4242587fF"
    }
}
HEADERS = {
    "Accept": "application/json",
    "ContentType": "application/json",
    "authorization": None
}


def get_token():
    if HEADERS.get("authorization"):
        HEADERS.pop("authorization")
    req = requests.post(MOBRAND_LOGOIN_URL, json=USER_INFO.get("login_info"), headers=HEADERS, timeout=15)
    login_data = req.json()
    TOKEN["token"] = login_data["token"]
    TOKEN["login_time"] = datetime.datetime.now()


@track_router.post("/execute")
async def execute_track(query: SearchTrackLink = Depends(SearchTrackLink)):
    """
    执行追踪
    :return:
    """
    """
    1 获取token并判断token的有效期  token自定义有效期为2个小时
    2 根据用户输入的参数 抓取第三方接口响应数据
    3 添加异常处理
    :return:
    """
    # 1 校验token时间
    print(query.platform.name)
    if "login_time" in TOKEN:
        login_time = TOKEN.get('login_time')
        current_time = datetime.datetime.now()
        if (current_time - login_time).seconds > 60 * 60 * 2:
            get_token()
    else:
        get_token()
    # 构建查询参数 并且抓取返回结果
    prams = {
        "userid": USER_INFO.get("user_id"),
        "url": query.url,
        "platform": query.platform.name,
        "country": query.country.name,
    }
    # 够间headers
    HEADERS["authorization"] = "Bearer " + TOKEN["token"]
    # 请求
    req = requests.post(MOBRAND_TRACK_URL, json=prams, headers=HEADERS, timeout=15)
    spider_data = req.json()
    return spider_data
