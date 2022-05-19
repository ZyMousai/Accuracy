# offers账号管理
from typing import List
from app.OffersSystem.OffersUnion.DataValidation import OffersUnionSearch, AddOffersUnion, UpdateOffersUnion
from sql_models.OffersSystem.OrmOffersSystem import OffersAccount
from fastapi import APIRouter, Depends,HTTPException

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
async def search_offers_account(search_info: OffersUnionSearch = Depends(OffersUnionSearch), dbs=Depends(db_session)):
    filter_condition = [
        ('union_name', f'.like(f"%{search_info.union_name}%")', search_info.union_name),
        ('offers_account', f'.like(f"%{search_info.union_name}%")', search_info.union_name),
        ("created_time", f'>="{search_info.start_time}"', search_info.start_time),
        ("created_time", f'<="{search_info.end_time}"', search_info.end_time),
        ("is_delete", '==0', 0),
        ("status", f'=={search_info.status}', search_info.union_system_id)
    ]
    result, count, total_page = await OffersAccount.get_all_detail_page(dbs, search_info.page, search_info.page_size,
                                                                      *filter_condition)
    response_json = {"total": count,
                     "page": search_info.page,
                     "page_size": search_info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@offers_account_router.get('/detail')
async def get_offers_account_one(offers_account_id: int, dbs=Depends(db_session)):
    result = await OffersAccount.get_one_detail(dbs, offers_account_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    return result


@offers_account_router.post('/')
async def add_offers_account_id(info: AddOffersUnion, dbs=Depends(db_session)):
    offers_union_id = await OffersAccount.add_data(dbs, info)
    if not offers_union_id:
        raise HTTPException(status_code=403, detail="Duplicate posts.")
    response_json = info.dict()
    response_json["id"] = offers_union_id
    return response_json


@offers_account_router.patch('/')
async def update_offers_account(info: UpdateOffersUnion, dbs=Depends(db_session)):
    update_data_dict = info.dict(exclude_unset=True)
    result = await OffersAccount.update_data(dbs, update_data_dict, is_delete=0)
    if not result:
        raise HTTPException(status_code=403, detail="offers_union does not exist.")
    return result
