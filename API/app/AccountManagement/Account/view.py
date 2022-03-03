# Account 视图
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.AccountManagement.Account.DataValidation import SearchAccount, AddAccount, UpdateAccount
from sql_models.AccountManagement.OrmAccountManagement import Account
from sql_models.PersonnelManagement.OrmPersonnelManagement import *
from sql_models.db_config import db_session
from util.crypto import encrypt, decrypt

account_router = APIRouter(
    prefix="/account/v1",
    responses={404: {"description": "Not found"}},
    tags=["AccountManagement"])


@account_router.get("/")
async def get_account(info: SearchAccount = Depends(SearchAccount),
                      dbs: AsyncSession = Depends(db_session)):
    filter_condition = [
        ('account', f'.like(f"%{info.account}%")', info.account),
        ('platform', f'.like(f"%{info.platform}%")', info.platform),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await Account.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@account_router.get("/{account_id}")
async def get_account_one(account_id: int,
                          dbs: AsyncSession = Depends(db_session)):
    result = await Account.get_one_detail(dbs, account_id)
    filter_condition = [
        ("account_id", f"=={result.id}", result.id)
    ]
    # noinspection PyBroadException
    try:
        role_id = (await RoleAccountMapping.get_one(dbs, *filter_condition)).role_id
    except Exception as e:
        print(e)
        role_id = "unbound"
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    # 对account数据进行重新归纳赋值
    new_result = {
        "role_id": role_id,
        "account": result.account,
        "is_delete": result.is_delete,
        "id": result.id,
        "password": result.password,
        "remark": result.remark,
        "platform": result.platform,
    }
    return {"data": new_result}


@account_router.post("/")
async def add_account(info: AddAccount,
                      dbs: AsyncSession = Depends(db_session)):
    info.password = encrypt(info.password)
    account_id = await Account.add_data(dbs, info)
    response_json = info.dict()
    response_json["id"] = account_id
    return response_json


@account_router.patch("/")
async def update_account(info: UpdateAccount, dbs: AsyncSession = Depends(db_session)):
    """
    修改账号信息
    :param info:
    :param dbs:
    :return:
    """
    if info.password:
        info.password = encrypt(info.password)
    update_data_dict = info.dict(exclude_unset=True)
    if len(update_data_dict) > 1:
        result = await Account.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="Account does not exist.")
    response_json = {"data": update_data_dict}
    return response_json


@account_router.delete("/")
async def delete_account(ids: Optional[List[int]] = Query(...), dbs: AsyncSession = Depends(db_session)):
    result = await Account.delete_data(dbs, tuple(ids), auto_commit=False)

    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    filter_condition = [
        ("account_id", f".in_({ids})", ids)
    ]
    await RoleAccountMapping.filter_delete_data(dbs, *filter_condition, auto_commit=True)
    # 删除跟角色关联
    response_json = {"data": ids}
    return response_json


# 暂时屏蔽解密接口
# @account_router.get("/password/{account_id}")
# async def decode_password(account_id: int, dbs: AsyncSession = Depends(db_session)):
#     result = await Account.get_one_detail(dbs, account_id)
#     result.password = decrypt(result.password)
#     return {"data": result.password}
