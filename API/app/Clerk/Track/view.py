# Track 视图
import datetime
import requests

from typing import Optional, List
from app.Clerk.Track.DataValidation import SearchTrackLink, AddTrackAlliance, UpdateTrackAlliance, AddTrackUrl, \
    SearchTrackAlliance
from sql_models.Clerk.OrmTrack import TrackAlliance, TrackUrl
from sql_models.db_config import db_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config import globals_config

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

USER_INFO = globals_config.USER_INFO

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


@track_router.get("/execute")
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
    # 构建headers
    HEADERS["authorization"] = "Bearer " + TOKEN["token"]
    # 请求
    req = requests.post(MOBRAND_TRACK_URL, json=prams, headers=HEADERS, timeout=15)
    spider_data = req.json()
    return spider_data


@track_router.post("/alliance")
async def create_alliance(info: AddTrackAlliance, dbs: AsyncSession = Depends(db_session)):
    return {"data": await TrackAlliance.add_data(dbs, info)}


@track_router.delete("/alliance")
async def delete_alliance(ids: Optional[List[int]], dbs: AsyncSession = Depends(db_session)):
    await TrackAlliance.delete_data(dbs, ids, auto_commit=False)

    filter_c = [
        ("alliance_id", f".in_({ids})", ids)
    ]
    await TrackUrl.filter_delete_data(dbs, *filter_c, auto_commit=True)
    return {"data": ids}


@track_router.patch("/alliance")
async def update_alliance(info: UpdateTrackAlliance, dbs: AsyncSession = Depends(db_session)):
    update_data_dict = info.dict(exclude_unset=True)
    if len(update_data_dict) > 1:
        result = await TrackAlliance.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=404, detail="TrackAlliance does not exist.")
    response_json = {"data": update_data_dict}
    return response_json


@track_router.get("/alliance")
async def get_alliance(info: SearchTrackAlliance = Depends(SearchTrackAlliance),
                       dbs: AsyncSession = Depends(db_session)):
    #  需要联表查询
    filter_condition = {
        "name_or_url": info.name_or_url,
        "track_url": info.track_url
    }
    result, count, total_page = await TrackAlliance.get_all_detail_page_track(dbs, info.page, info.page_size,
                                                                              **filter_condition)

    # 整理查询出来的数据
    result_new = []
    ids = []
    for x in result:
        if x.id not in ids:
            ids.append(x.id)
            dd = {
                "id": x.id,
                "name": x.name,
                "url": x.url,
                "track_url": list()
            }
            for y in result:
                if x.id == y.id and y.track_url:
                    dd.get("track_url").append({"id": y.id_1, "track_url": y.track_url})
            result_new.append(dd)

    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result_new}
    return response_json


@track_router.post("/TrackUrl")
async def add_track_url(info: AddTrackUrl, dbs: AsyncSession = Depends(db_session)):
    result = await TrackAlliance.get_one_detail(dbs, info.alliance_id)
    if not result:
        raise HTTPException(status_code=404, detail="alliance_id does not exist.")
    return {"data": await TrackUrl.add_data(dbs, info)}


@track_router.delete("/TrackUrl")
async def delete_track_url(ids: Optional[List[int]], dbs: AsyncSession = Depends(db_session)):
    filter_c = [
        ("id", f".in_({ids})", ids)
    ]
    await TrackUrl.filter_delete_data(dbs, *filter_c, auto_commit=True)
    return {"data": ids}
