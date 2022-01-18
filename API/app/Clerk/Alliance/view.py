# Departments 视图
from sql_models.CardManagement.OrmCardManagement import TbAlliance
from app.Clerk.Alliance.DataValidation import AddAlliance, UpdateAlliance, SearchAlliance
from sqlalchemy.ext.asyncio import AsyncSession
from sql_models.db_config import db_session
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from typing import Optional, List

clerk_alliance_router = APIRouter(
    prefix="/alliance/v1",
    responses={404: {"alliance": "Not found"}}, )


@clerk_alliance_router.get('/')
async def get_alliance(info: SearchAlliance = Depends(SearchAlliance), dbs: AsyncSession = Depends(db_session), ):
    """
    获取联盟列表
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('alliance_name', f'.like(f"%{info.alliance_name}%")', info.alliance_name),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await TbAlliance.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@clerk_alliance_router.get('/{alliance_id}')
async def get_alliance_one(alliance_id: int = Path(..., title='联盟id', description="联盟id", ge=1),
                          dbs: AsyncSession = Depends(db_session)):
    """
    获取某个联盟的信息
    :param alliance_id:
    :param dbs:
    :return:
    """
    result = await TbAlliance.get_one_detail(dbs, alliance_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


@clerk_alliance_router.delete('/')
async def delete_alliance(ids: List[int] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
    删除联盟 可批量
    :param ids:
    :param dbs:
    :return:
    """
    result = await TbAlliance.delete_data_logic(dbs, tuple(ids))
    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    response_json = {"data": ids}
    return response_json


@clerk_alliance_router.post('/')
async def create_alliance(info: AddAlliance, dbs: AsyncSession = Depends(db_session)):
    """
    创建联盟
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('alliance_name', f'=="{info.alliance_name}"', info.alliance_name)
    ]
    result = await TbAlliance.get_one(dbs, *filter_condition)
    if result:
        raise HTTPException(status_code=403, detail="Duplicate alliance.")
    result = await TbAlliance.add_data(dbs, info)
    response_json = {"data": result}
    return response_json


@clerk_alliance_router.patch('/')
async def update_alliance(info: UpdateAlliance, dbs: AsyncSession = Depends(db_session)):
    """
    修改联盟信息
    :param info:
    :param dbs:
    :return:
    """
    update_data_dict = info.dict(exclude_unset=True)
    filter_condition = [
        ('alliance_name', f'=="{info.alliance_name}"', info.alliance_name)
    ]
    result = await TbAlliance.get_one(dbs, *filter_condition)
    if result:
        raise HTTPException(status_code=403, detail="Duplicate alliance.")
    if len(update_data_dict) > 1:
        result = await TbAlliance.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="alliance does not exist.")
    response_json = {"data": update_data_dict}
    return response_json
