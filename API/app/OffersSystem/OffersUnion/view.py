# offers联盟管理
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.OffersSystem.OffersUnion.DataValidation import OffersUnionSearch, AddOffersUnion, UpdateOffersUnion
from sql_models.OffersSystem.OrmOffersSystem import OffersUnion, UnionSystem

from sql_models.db_config import db_session

offers_union_router = APIRouter(
    prefix="/OffersUnion/v1",
    responses={404: {"description": "Not found"}},
    tags=["OffersUnion"])


@offers_union_router.delete("/")
async def delete_offers_union(offers_union_ids: List[int], dbs=Depends(db_session)):
    result = await OffersUnion.delete_data(dbs, tuple(offers_union_ids), auto_commit=False)
    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    return result


@offers_union_router.get('/')
async def search_offers_union(search_info: OffersUnionSearch = Depends(OffersUnionSearch), dbs=Depends(db_session)):
    filter_condition = [
        ('union_name', f'.like(f"%{search_info.union_name}%")', search_info.union_name),
        ("created_time", f'>="{search_info.start_time}"', search_info.start_time),
        ("created_time", f'<="{search_info.end_time}"', search_info.end_time),
        ("is_delete", '==0', 0),
        ("union_system_id", f'=={search_info.union_system_id}', search_info.union_system_id)
    ]
    result, count, total_page = await OffersUnion.get_all_detail_page_associated(dbs, search_info.page,
                                                                                 search_info.page_size,
                                                                                 *filter_condition)
    response_json = {"total": count,
                     "page": search_info.page,
                     "page_size": search_info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@offers_union_router.get('/detail')
async def get_offers_union_one(offers_union_id: int, dbs=Depends(db_session)):
    result = await OffersUnion.get_one_detail(dbs, offers_union_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    return result


@offers_union_router.post('/')
async def add_offers_union_id(info: AddOffersUnion, dbs=Depends(db_session)):
    offers_union_id = await OffersUnion.add_data(dbs, info)
    if not offers_union_id:
        raise HTTPException(status_code=403, detail="Duplicate posts.")
    response_json = info.dict()
    response_json["id"] = offers_union_id
    return response_json


@offers_union_router.patch('/')
async def update_offers_union(info: UpdateOffersUnion, dbs=Depends(db_session)):
    update_data_dict = info.dict(exclude_unset=True)
    result = await OffersUnion.update_data(dbs, update_data_dict, is_delete=0)
    if not result:
        raise HTTPException(status_code=403, detail="offers_union does not exist.")
    return result


@offers_union_router.get('/union_system')
async def search_offers_union(dbs=Depends(db_session)):
    result = await OffersUnion.get_all(dbs, *[("is_delete", '==0', 0)])
    response_json = {"data": result}
    return response_json
