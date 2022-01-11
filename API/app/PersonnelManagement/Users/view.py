# Users 视图
from fastapi import APIRouter, Depends, Query, HTTPException, Request

from typing import Optional, List
from util.crypto import sha1_encode
from app.PersonnelManagement.Users.DataValidation import AddUser, UpdateUser, UpdatePassword, SearchUser
from sql_models.PersonnelManagement.OrmUsers import Users
from sqlalchemy.ext.asyncio import AsyncSession
from sql_models.db_config import db_session

users_router = APIRouter(
    prefix="/users/v1",
    responses={404: {"description": "Not found"}}, )


@users_router.get('/')
async def get_user(info: SearchUser = Depends(SearchUser),
                   dbs: AsyncSession = Depends(db_session)):
    """
    获取用户列表
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = {
        'name': [f'.like(f"%{info.name}%")', info.name],
        'gender': [f'=={info.gender}', info.gender],
        'creator': [f'.like(f"%{info.creator}%")', info.creator]
    }
    result, count, total_page = await Users.get_all_detail_page(dbs, info.page, info.page_size, **filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@users_router.get('/{user_id}')
async def get_user_one(user_id: Optional[int] = Query(None), dbs: AsyncSession = Depends(db_session)):
    """
    获取某个用户的信息
    :param user_id:
    :param dbs:
    :return:
    """
    result = await Users.get_one_detail(dbs, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


@users_router.delete('/')
async def delete_users(ids: Optional[List[int]] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
    删除用户 可批量
    :param ids:
    :param dbs:
    :return:
    """
    result = await Users.delete_data_logic(dbs, tuple(ids))
    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    response_json = {"data": ids}
    return response_json


@users_router.post('/')
async def create_user(request: Request, user: AddUser, dbs: AsyncSession = Depends(db_session)):
    """
    创建用户
    :param request:
    :param user:
    :param dbs:
    :return:
    """
    user.creator = request.state.username
    result = await Users.add_data(dbs, user)
    if not result:
        raise HTTPException(status_code=403, detail="Duplicate account.")
    response_json = {"data": result}
    return response_json


@users_router.patch('/')
async def update_user(user: UpdateUser, dbs: AsyncSession = Depends(db_session)):
    """
    修改用户信息
    :param user:
    :param dbs:
    :return:
    """
    update_data_dict = user.dict(exclude_unset=True)
    if len(update_data_dict) > 1:
        result = await Users.update_data(dbs, update_data_dict)
        if not result:
            raise HTTPException(status_code=403, detail="User does not exist.")
    response_json = {"data": update_data_dict}
    return response_json


@users_router.patch('/password')
async def update_password(info: UpdatePassword, dbs: AsyncSession = Depends(db_session)):
    """
    修改密码
    :param info:
    :param dbs:
    :return:
    """
    info.password = sha1_encode(info.password)
    update_data_dict = info.dict()
    result = await Users.update_data(dbs, update_data_dict)
    if not result:
        raise HTTPException(status_code=403, detail="User does not exist.")
    response_json = {"data": info.id}
    return response_json


@users_router.post('/login')
async def update_password(dbs: AsyncSession = Depends(db_session)):
    """
    登录
    :param dbs:
    :return:
    """
    return dbs
