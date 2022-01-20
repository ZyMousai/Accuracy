import requests
from fastapi import APIRouter, Depends
from datetime import datetime
from config import globals_config
from app.PcTrackDomain.schemas import SearchTrackLink

trackingLink_router = APIRouter(
    prefix="/trackinglink/v1",
    responses={404: {"description": "Not found"}}, )

# 登录url
MOBRAND_LOGOIN_URL = "https://api.mobrand.net/login"
# 抓取url
MOBRAND_TRACK_URL = "https://api.offertest.net/offertest/console"

# token
TOKEN = dict()


def login_mobrand():
    parms = {
        "email": globals_config.EMAIL,
        "password": globals_config.PWD
    }
    headers = {
        "Accept": "application/json",
        "ContentType": "application/json"
    }
    req = requests.post(MOBRAND_LOGOIN_URL, json=parms, headers=headers, timeout=15)
    login_data = req.json()
    TOKEN["token"] = login_data["token"]
    TOKEN["login_time"] = datetime.now()


@trackingLink_router.get("/")
async def get_tracking_link_result(query: SearchTrackLink = Depends(SearchTrackLink)):
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
        current_time = datetime.now()
        if (current_time - login_time).seconds > 60 * 60 * 2:
            login_mobrand()
    else:
        login_mobrand()
    # 构建查询参数 并且抓取返回结果
    parms = {
        "userid": globals_config.USER_ID,
        "url": query.url,
        "platform": query.platform.name,
        "country": query.country.name,
    }
    headers = {
        "Accept": "application/json",
        "ContentType": "application/json",
        "authorization": "Bearer " + TOKEN["token"]
    }
    req = requests.post(MOBRAND_TRACK_URL, json=parms, headers=headers, timeout=15)
    spider_data = req.json()
    return spider_data
