# Departments 视图
from sql_models.CardManagement.OrmCardManagement import TbAccount
from app.Clerk.Account.DataValidation import AddAccount, UpdateAccount, SearchAccount
from sqlalchemy.ext.asyncio import AsyncSession
from sql_models.db_config import db_session
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List

account_router = APIRouter(
    prefix="/account/v1",
    responses={404: {"account": "Not found"}}, )


@account_router.get('/')
async def get_departments(info: SearchAccount = Depends(SearchAccount), dbs: AsyncSession = Depends(db_session), ):
    """
    获取账号列表
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('department', f'.like(f"%{info.account_name}%")', info.account_name),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await TbAccount.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@account_router.get('/{account_id}')
async def get_departments_one(account_id: Optional[int] = Query(None), dbs: AsyncSession = Depends(db_session)):
    """
    获取某个账号的信息
    :param account_id:
    :param dbs:
    :return:
    """
    result = await TbAccount.get_one_detail(dbs, account_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


@account_router.delete('/')
async def delete_departments(ids: Optional[List[int]] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
    删除账号 可批量
    :param ids:
    :param dbs:
    :return:
    """
    result = await TbAccount.delete_data_logic(dbs, tuple(ids))
    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    response_json = {"data": ids}
    return response_json


@account_router.post('/')
async def create_departments(user: AddAccount, dbs: AsyncSession = Depends(db_session)):
    """
    创建账号
    :param user:
    :param dbs:
    :return:
    """
    result = await TbAccount.add_data(dbs, user)
    if not result:
        raise HTTPException(status_code=403, detail="Duplicate account.")
    response_json = {"data": result}
    return response_json


@account_router.patch('/')
async def update_departments(user: UpdateAccount, dbs: AsyncSession = Depends(db_session)):
    """
    修改账号信息
    :param user:
    :param dbs:
    :return:
    """
    update_data_dict = user.dict(exclude_unset=True)
    if len(update_data_dict) > 1:
        result = await TbAccount.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="User does not exist.")
    response_json = {"data": update_data_dict}
    return response_json
