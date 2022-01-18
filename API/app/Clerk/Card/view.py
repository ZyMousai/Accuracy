# Departments 视图
from sql_models.CardManagement.OrmCardManagement import TbCard
from app.Clerk.Card.DataValidation import AddCard, UpdateCard, SearchCard
from sqlalchemy.ext.asyncio import AsyncSession
from sql_models.db_config import db_session
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from typing import Optional, List

clerk_card_router = APIRouter(
    prefix="/card/v1",
    responses={404: {"card": "Not found"}}, )


@clerk_card_router.get('/')
async def get_card(info: SearchCard = Depends(SearchCard), dbs: AsyncSession = Depends(db_session), ):
    """
    获取卡号列表
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('card_number', f'.like(f"%{info.card_number}%")', info.card_number),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await TbCard.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@clerk_card_router.get('/{card_id}')
async def get_card_one(card_id: int = Path(..., title='卡号id', description="卡号id", ge=1),
                       dbs: AsyncSession = Depends(db_session)):
    """
    获取某个卡号的信息
    :param card_id:
    :param dbs:
    :return:
    """
    result = await TbCard.get_one_detail(dbs, card_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


@clerk_card_router.delete('/')
async def delete_card(ids: List[int] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
    删除卡号 可批量
    :param ids:
    :param dbs:
    :return:
    """
    result = await TbCard.delete_data_logic(dbs, tuple(ids))
    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    response_json = {"data": ids}
    return response_json


@clerk_card_router.post('/')
async def create_card(info: AddCard, dbs: AsyncSession = Depends(db_session)):
    """
    创建卡号
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('card_number', f'=="{info.card_number}"', info.card_number)
    ]
    result = await TbCard.get_one(dbs, *filter_condition)
    if result:
        raise HTTPException(status_code=403, detail="Duplicate card.")
    result = await TbCard.add_data(dbs, info)
    response_json = {"data": result}
    return response_json


@clerk_card_router.patch('/')
async def update_card(info: UpdateCard, dbs: AsyncSession = Depends(db_session)):
    """
    修改卡号信息
    :param info:
    :param dbs:
    :return:
    """
    update_data_dict = info.dict(exclude_unset=True)
    filter_condition = [
        ('card_number', f'=="{info.card_number}"', info.card_number)
    ]
    result = await TbCard.get_one(dbs, *filter_condition)
    if result:
        raise HTTPException(status_code=403, detail="Duplicate card.")
    if len(update_data_dict) > 1:
        result = await TbCard.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="card does not exist.")
    response_json = {"data": update_data_dict}
    return response_json
