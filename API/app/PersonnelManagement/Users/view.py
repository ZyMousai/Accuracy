# Users 视图

from fastapi import APIRouter, Depends, Query, HTTPException

from typing import Optional, List

from fastapi.security import OAuth2PasswordRequestForm
from app.PersonnelManagement.Users.permissions import Permissions
from util.crypto import sha1_encode
from app.PersonnelManagement.Users.DataValidation import AddUser, UpdateUser, UpdatePassword, SearchUser
from sql_models.PersonnelManagement.OrmPersonnelManagement import Users, Roles, RoleUserMapping, DepartmentUserMapping
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
    filter_condition = [
        ('name', f'.like(f"%{info.name}%")', info.name),
        ('gender', f'=={info.gender}', info.gender),
        ('creator', f'.like(f"%{info.creator}%")', info.creator),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await Users.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
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
    result = await Users.delete_data_logic(dbs, tuple(ids), auto_commit=False)

    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    filter_condition = [
        ("user_id", f".in_({ids})", ids)
    ]
    # 删除角色关联
    await RoleUserMapping.filter_delete_data(dbs, *filter_condition, auto_commit=False)
    # 删除部门关联
    await DepartmentUserMapping.filter_delete_data(dbs, *filter_condition, auto_commit=True)
    response_json = {"data": ids}
    return response_json


@users_router.post('/')
async def create_user(user: AddUser, dbs: AsyncSession = Depends(db_session)):
    """
    创建用户
    :param user:
    :param dbs:
    :return:
    """
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
        result = await Users.update_data(dbs, update_data_dict, is_delete=0)
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
    result = await Users.update_data(dbs, update_data_dict, is_delete=0)
    if not result:
        raise HTTPException(status_code=403, detail="User does not exist.")
    response_json = {"data": info.id}
    return response_json


async def authenticate(dbs, username: str, password: str):
    """用户校验"""
    filter_condition = [
        ('account', f'=="{username}"', username),
        ('is_delete', '==0', 0)
    ]

    user = await Users.get_one(dbs, *filter_condition)

    if not user:
        return False
    if not sha1_encode(password) == user.password:
        return False
    return user


@users_router.post('/login')
async def login(dbs: AsyncSession = Depends(db_session),
                form_data: OAuth2PasswordRequestForm = Depends()):
    """
    登录
    :param dbs:
    :param form_data:
    :return:
    """
    # 校验用户密码逻辑, 返回user_id
    user: Users = await authenticate(dbs, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail='Account password verification failed.')

    role: Roles = await Roles.get_role_user(dbs, user.id)

    # 使用user_id生成jwt token
    data = {'user_id': user.id, "account": user.account, "name": user.name, "role_id": role.id, "role": role.role}
    token = await Permissions.create_jwt_token(data)
    # 存到redis有效期三天
    # await request.app.state.redis.get(token)
    # print("正在把token加入redis中: " + token)
    # await request.app.state.redis.set(key=token, value=data, seconds=24 * 60 * 60 * 3)
    # await request.app.state.redis.expire(token, 24 * 60 * 60 * 3)
    # print("加入完成")
    # await request.app.state.redis.get(user.email)
    # noinspection PyArgumentList
    return {"access_token": token, "token_type": "bearer"}
