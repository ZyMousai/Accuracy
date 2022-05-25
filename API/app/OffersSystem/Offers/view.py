# offers联盟管理
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.OffersSystem.Offers.DataValidation import UpdateOffers, SearchOffers
from app.OffersSystem.Offers.spider import UnionApi
from sql_models.OffersSystem.OrmOffersSystem import Offers
from sql_models.db_config import db_session

offers_router = APIRouter(
    prefix="/Offers/v1",
    responses={404: {"description": "Not found"}},
    tags=["Offers"])


@offers_router.get('/')
async def get_user(info: SearchOffers = Depends(SearchOffers),
                   dbs: AsyncSession = Depends(db_session)):
    """
    获取offer列表
    :param info:
    :param dbs:
    :return:
    """

    filter_condition = [
        ('union_id', f'=={info.union_id}', info.union_id),
        ('account_id', f'=={info.account_id}', info.account_id),
        ('offers_name', f'.like(f"%{info.offers_name}%")', info.offers_name),
        ('pay', f'{info.pay_filter}{info.pay}', info.pay),
        ('country', f'.like(f"%{info.country}%")', info.country),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await Offers.get_all_detail_page_associated(dbs, info.page, info.page_size,
                                                                            *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@offers_router.patch('/')
async def update_offer(offers: UpdateOffers, dbs: AsyncSession = Depends(db_session)):
    """
    修改offers
    :param offers:
    :param dbs:
    :return:
    """
    update_data_dict = offers.dict(exclude_unset=True)
    if len(update_data_dict) > 1:
        result = await Offers.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="offer does not exist.")
    response_json = {"data": update_data_dict}
    return response_json
