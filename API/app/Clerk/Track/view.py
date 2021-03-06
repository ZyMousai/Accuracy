# Track 视图
import datetime
import requests
import uuid

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
        执行追踪:
        1 获取token并判断token的有效期  token自定义有效期为2个小时
        2 根据用户输入的参数 抓取第三方接口响应数据
        3 添加异常处理
    :param query:

        执行所需参数

    :return:

        执行完成后返回的数据
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
    """
        新建联盟

    :param info:

        添加的参数

    :param dbs:

        数据库依赖

    :return:

        添加到表后的id
    """
    # 生成特殊的uuid作为唯一标识
    uuid_ins = str(uuid.uuid1())
    filter_condition = {
        'name': info.name,
        'url': info.url,
        'alliance_uuid': uuid_ins,
    }
    return {"data": await TrackAlliance.add_data(dbs, filter_condition)}


@track_router.delete("/alliance")
async def delete_alliance(ids: Optional[List[int]], dbs: AsyncSession = Depends(db_session)):
    """
        真实删除联盟

    :param ids:

        需要删除的联盟id

    :param dbs:

        数据库依赖

    :return:

        被删除的联盟的id
    """
    # 获取到每个track_alliance表的alliance_id,通过alliance_id去删除track_url里的数据
    filter_condition = [
        ("id", f".in_({ids})", ids)
    ]
    alliance_uuid_list = [i.alliance_uuid for i in (await TrackAlliance.get_all(dbs, *filter_condition))]
    await TrackAlliance.delete_data(dbs, ids, auto_commit=False)
    filter_c = [
        ("alliance_id", f".in_({alliance_uuid_list})", alliance_uuid_list)
    ]
    await TrackUrl.filter_delete_data(dbs, *filter_c, auto_commit=True)
    return {"data": ids, "alliance_ids": alliance_uuid_list}


@track_router.patch("/alliance")
async def update_alliance(info: UpdateTrackAlliance, dbs: AsyncSession = Depends(db_session)):
    """
        更新联盟信息

    :param info:

        需要被更新的信息

    :param dbs:

        数据库依赖

    :return:

        更新的信息参数
    """
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
    """
        获取联盟信息

    :param info:

        需要查询的参数

    :param dbs:

        数据库依赖

    :return:

        包含分页分页信息的联盟列表
    """
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
                    dd.get("track_url").append(
                        {
                            "id": y.id_1,
                            "track_url": y.track_url
                        }
                    )  # 这里的id_1是联表查询的副表的id
            result_new.append(dd)

    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result_new}
    return response_json


@track_router.post("/TrackUrl")
async def add_track_url(info: AddTrackUrl, dbs: AsyncSession = Depends(db_session)):
    """
        添加追踪链接

    :param info:

        需要被追踪的链接

    :param dbs:

        数据库依赖

    :return:

        添加到表里的链接的id
    """
    result = await TrackAlliance.get_one_detail(dbs, info.alliance_id)
    if not result:
        raise HTTPException(status_code=404, detail="alliance_id does not exist.")
    # 获得track_alliance的alliance_uuid,添加到track_url的alliance_id
    add_track_url_dict = {
        "track_url": info.track_url,
        "alliance_id": result.alliance_uuid
    }
    return {"data": await TrackUrl.add_data(dbs, add_track_url_dict)}


@track_router.delete("/TrackUrl")
async def delete_track_url(ids: Optional[List[int]], dbs: AsyncSession = Depends(db_session)):
    """
        真实删除追踪链接

    :param ids:

        需要删除的链接的id

    :param dbs:

        数据库依赖

    :return:

        被删除的id
    """
    filter_c = [
        ("id", f".in_({ids})", ids)
    ]
    await TrackUrl.filter_delete_data(dbs, *filter_c, auto_commit=True)
    return {"data": ids}
