# offers账号管理
from typing import List
from util.crypto import encrypt, decrypt
from app.OffersSystem.OffersAccount.DataValidation import OffersAccountSearch, AddOffersAccount, UpdateOffersAccount
from sql_models.OffersSystem.OrmOffersSystem import OffersAccount
from fastapi import APIRouter, Depends, HTTPException

from sql_models.db_config import db_session

offers_account_router = APIRouter(
    prefix="/OffersAccount/v1",
    responses={404: {"description": "Not found"}},
    tags=["OffersAccount"])


@offers_account_router.delete("/")
async def delete_offers_account(offers_account_ids: List[int], dbs=Depends(db_session)):
    result = await OffersAccount.delete_data(dbs, tuple(offers_account_ids), auto_commit=False)
    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    return result


@offers_account_router.get('/')
async def search_offers_account(search_info: OffersAccountSearch = Depends(OffersAccountSearch),
                                dbs=Depends(db_session)):
    filter_condition = [
        ('OffersUnion.union_name', f'.like(f"%{search_info.union_name}%")', search_info.union_name),
        ('cls.offers_account', f'.like(f"%{search_info.offers_account}%")', search_info.offers_account),
        ("cls.created_time", f'>="{search_info.start_time}"', search_info.start_time),
        ("cls.created_time", f'<="{search_info.end_time}"', search_info.end_time),
        ("cls.is_delete", '==0', 0),
        ("cls.status", f'=={search_info.status}', search_info.status)
    ]
    result, count, total_page = await OffersAccount.get_all_detail_page_associated(dbs, search_info.page,
                                                                                   search_info.page_size,
                                                                                   *filter_condition)

    response_json = {"total": count,
                     "page": search_info.page,
                     "page_size": search_info.page_size,
                     "total_page": total_page,
                     "data": [{
                         "id": i.id,
                         "union_name": i.union_name,
                         "offers_account": i.offers_account,
                         "offers_pwd": decrypt(i.offers_pwd),
                         "offers_api_key": i.offers_api_key,
                         "status": i.status,
                     } for i in result]
                     }
    return response_json


@offers_account_router.get('/detail')
async def get_offers_account_one(offers_account_id: int, dbs=Depends(db_session)):
    result = await OffersAccount.get_one_detail(dbs, offers_account_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    return result


@offers_account_router.post('/')
async def add_offers_account_id(info: AddOffersAccount, dbs=Depends(db_session)):
    info.offers_pwd = encrypt(info.offers_pwd)
    offers_union_id = await OffersAccount.add_data(dbs, info)
    if not offers_union_id:
        raise HTTPException(status_code=403, detail="Duplicate offers_account.")
    response_json = info.dict()
    response_json["id"] = offers_union_id
    return response_json


@offers_account_router.patch('/')
async def update_offers_account(info: UpdateOffersAccount, dbs=Depends(db_session)):
    if info.offers_pwd:
        info.offers_pwd = encrypt(info.offers_pwd)
    update_data_dict = info.dict(exclude_unset=True)
    result = await OffersAccount.update_data(dbs, update_data_dict, is_delete=0)
    if not result:
        raise HTTPException(status_code=403, detail="offers_account does not exist.")
    return result
