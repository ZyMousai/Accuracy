# Users 视图
from fastapi import APIRouter, Depends, Query

from typing import Optional, List
from sql_models.PersonnelManagement.OrmUsers import Users
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from sql_models.db_config import db_session

users_router = APIRouter(
    prefix="/users/v1",
    responses={404: {"description": "Not found"}}, )


@users_router.get('/')
async def get_user(page: Optional[int] = 1, page_size: Optional[int] = 10, dbs: AsyncSession = Depends(db_session)):
    result, count, total_page = await Users.get_all_detail_page(dbs, page, page_size)
    response_json = {"total": count,
                     "page": page,
                     "page_size": page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@users_router.get('/{user_id}')
async def get_user_one(user_id: Optional[int] = Query(None), dbs: AsyncSession = Depends(db_session)):
    return await Users.get_one_detail(dbs, user_id)


@users_router.delete('/')
async def delete_users(ids: Optional[List[int]] = Query(...), dbs: AsyncSession = Depends(db_session)):
    return await Users.delete_data_logic(dbs, tuple(ids))
