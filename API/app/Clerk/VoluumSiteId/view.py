# VoluumSiteId 视图
import random
from typing import Optional, List

from app.Clerk.VoluumSiteId.DataValidation import AddCampaignMapping, SearchCampaignMapping
from app.Clerk.VoluumSiteId.VoluumSpider import VoluumSpider
from config import globals_config
from sql_models.Clerk.OrmVoluumSiteId import DBCampaignMapping
from sql_models.db_config import db_session
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from util.mongo_c.MongoClient import MongoClient

voluum_router = APIRouter(
    prefix="/voluum/v1",
    responses={404: {"description": "Not found"}},
    tags=["Voluum"])


@voluum_router.get('/campaign_site_url/{m_id}/{s_id}')
async def get_campaign_site_url(m_id: str, s_id: str, dbs: AsyncSession = Depends(db_session)):
    """生成携带site-id的campaign_url"""

    # 1. 拿到数据 可以获取到此campaign_id最近的site-id
    ax = VoluumSpider()
    ax.get_token()
    body = ax.get_one_reports(m_id)['body']

    # 2. 根据 uniqueClicks 进行排序获取 site-id
    c_c = {i['customVariable2']: i['uniqueClicks'] for i in body if i['customVariable2'].isdigit()}
    c_c_sort = {k: v for k, v in sorted(c_c.items(), key=lambda item: item[1], reverse=True)}

    site_id_list = []

    for x, v in c_c_sort.items():
        if int(v) == 0:
            continue
        elif x.isdigit():
            site_id_list.append(x)
        else:
            pass

    if len(site_id_list) > 4:
        site_id = random.choice(site_id_list[4:10])
    else:
        site_id = random.choice(site_id_list[:-3:-1])

    # 3. 根据campaigns-id获取url
    # 通过主id拿到从id，查询主id最近的site，但是更换的链接是从id
    # filter_c = [
    #     ("m_id", f"=='{m_id}'", m_id),
    #     ("s_id", f"=='{s_id}'", s_id)
    # ]
    # cam_m_s_mapping = await DBCampaignMapping.get_one(dbs, *filter_c)
    mongo = MongoClient(**globals_config.MONGO_INFO.__dict__)
    query_ = mongo.select('voluum_campaigns', **{'id': s_id})[0]
    url = query_['impressionUrl'].replace('{site_id}', site_id)
    if '/impression' in url:
        url = url.replace('/impression', '')

    return {"data": url}


@voluum_router.get('/campaign_mapping')
async def get_campaign_mapping(info: SearchCampaignMapping = Depends(SearchCampaignMapping),
                               dbs: AsyncSession = Depends(db_session)):
    """
    获取角色列表
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('m_name', f'.like(f"%{info.m_name}%")', info.m_name),
        ('s_name', f'.like(f"%{info.s_name}%")', info.s_name),
        ('m_id', f'=="{info.m_id}"', info.m_id),
        ('s_id', f'=="{info.s_id}"', info.s_id),
    ]
    result, count, total_page = await DBCampaignMapping.get_all_detail_page(dbs, info.page, info.page_size,
                                                                            *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@voluum_router.post('/campaign_mapping')
async def add_campaign_mapping(info: AddCampaignMapping, dbs: AsyncSession = Depends(db_session)):
    return {"data": await DBCampaignMapping.add_data(dbs, info)}


@voluum_router.delete("/campaign_mapping")
async def delete_campaign_mapping(ids: Optional[List] = Query(...), dbs: AsyncSession = Depends(db_session)):
    return {"data": await DBCampaignMapping.delete_data(dbs, ids)}
