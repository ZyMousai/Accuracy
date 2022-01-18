# Card视图
from sql_models.Clerk.OrmCardManagement import *
from app.Clerk.Card.DataValidation import *
from sqlalchemy.ext.asyncio import AsyncSession
from sql_models.db_config import db_session
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from typing import List

clerk_card_router = APIRouter(
    prefix="/card/v1",
    responses={404: {"card": "Not found"}},
    tags=["Card"])


@clerk_card_router.get('/card')
async def get_card(info: SearchCard = Depends(SearchCard), dbs: AsyncSession = Depends(db_session), ):
    """
    获取卡号列表
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('card_number', f'.like("%{info.card_number}%")', info.card_number),
        ('is_delete', '==0', 0),
        ('retain', f'=={info.retain}', info.retain),
        ('card_status', f'=={info.card_status}', info.card_status),
    ]
    result, count, total_page = await TbCard.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@clerk_card_router.get('/card/{card_id}')
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


@clerk_card_router.delete('/card')
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


@clerk_card_router.post('/card')
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


@clerk_card_router.patch('/card')
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


@clerk_card_router.get('/account')
async def get_account(info: SearchAccount = Depends(SearchAccount), dbs: AsyncSession = Depends(db_session), ):
    """
    获取账号列表
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('account_name', f'.like("%{info.account_name}%")', info.account_name),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await TbAccount.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@clerk_card_router.get('/account/{account_id}')
async def get_account_one(account_id: int = Path(..., title='账号id', description="账号id", ge=1),
                          dbs: AsyncSession = Depends(db_session)):
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


@clerk_card_router.delete('/account')
async def delete_account(ids: List[int] = Query(...), dbs: AsyncSession = Depends(db_session)):
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


@clerk_card_router.post('/account')
async def create_account(user: AddAccount, dbs: AsyncSession = Depends(db_session)):
    """
    创建账号
    :param user:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('account_name', f'=="{user.account_name}"', user.account_name)
    ]
    result = await TbAccount.get_one(dbs, *filter_condition)
    if result:
        raise HTTPException(status_code=403, detail="Duplicate account.")
    result = await TbAccount.add_data(dbs, user)
    response_json = {"data": result}
    return response_json


@clerk_card_router.patch('/account')
async def update_account(user: UpdateAccount, dbs: AsyncSession = Depends(db_session)):
    """
    修改账号信息
    :param user:
    :param dbs:
    :return:
    """
    update_data_dict = user.dict(exclude_unset=True)
    filter_condition = [
        ('account_name', f'=="{user.account_name}"', user.account_name)
    ]
    result = await TbAccount.get_one(dbs, *filter_condition)
    if result:
        raise HTTPException(status_code=403, detail="Duplicate account.")
    if len(update_data_dict) > 1:
        result = await TbAccount.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="User does not exist.")
    response_json = {"data": update_data_dict}
    return response_json


@clerk_card_router.get('/alliance')
async def get_alliance(info: SearchAlliance = Depends(SearchAlliance), dbs: AsyncSession = Depends(db_session), ):
    """
    获取联盟列表
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('alliance_name', f'.like("%{info.alliance_name}%")', info.alliance_name),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await TbAlliance.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@clerk_card_router.get('/alliance/{alliance_id}')
async def get_alliance_one(alliance_id: int = Path(..., title='联盟id', description="联盟id", ge=1),
                           dbs: AsyncSession = Depends(db_session)):
    """
    获取某个联盟的信息
    :param alliance_id:
    :param dbs:
    :return:
    """
    result = await TbAlliance.get_one_detail(dbs, alliance_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


@clerk_card_router.delete('/alliance')
async def delete_alliance(ids: List[int] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
    删除联盟 可批量
    :param ids:
    :param dbs:
    :return:
    """
    result = await TbAlliance.delete_data_logic(dbs, tuple(ids))
    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    response_json = {"data": ids}
    return response_json


@clerk_card_router.post('/alliance')
async def create_alliance(info: AddAlliance, dbs: AsyncSession = Depends(db_session)):
    """
    创建联盟
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('alliance_name', f'=="{info.alliance_name}"', info.alliance_name)
    ]
    result = await TbAlliance.get_one(dbs, *filter_condition)
    if result:
        raise HTTPException(status_code=403, detail="Duplicate alliance.")
    result = await TbAlliance.add_data(dbs, info)
    response_json = {"data": result}
    return response_json


@clerk_card_router.patch('/alliance')
async def update_alliance(info: UpdateAlliance, dbs: AsyncSession = Depends(db_session)):
    """
    修改联盟信息
    :param info:
    :param dbs:
    :return:
    """
    update_data_dict = info.dict(exclude_unset=True)
    filter_condition = [
        ('alliance_name', f'=="{info.alliance_name}"', info.alliance_name)
    ]
    result = await TbAlliance.get_one(dbs, *filter_condition)
    if result:
        raise HTTPException(status_code=403, detail="Duplicate alliance.")
    if len(update_data_dict) > 1:
        result = await TbAlliance.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="alliance does not exist.")
    response_json = {"data": update_data_dict}
    return response_json


@clerk_card_router.get('/task')
async def get_task(info: SearchTask = Depends(SearchTask), dbs: AsyncSession = Depends(db_session), ):
    """
    获取任务列表
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('task', f'.like("%{info.task}%")', info.task),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await TbTask.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@clerk_card_router.get('/task/{task_id}')
async def get_task_one(task_id: int = Path(..., title='任务id', description="任务id", ge=1),
                       dbs: AsyncSession = Depends(db_session)):
    """
    获取某个任务的信息
    :param Task_id:
    :param dbs:
    :return:
    """
    result = await TbTask.get_one_detail(dbs, task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


@clerk_card_router.delete('/task')
async def delete_task(ids: List[int] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
    删除任务 可批量
    :param ids:
    :param dbs:
    :return:
    """
    result = await TbTask.delete_data_logic(dbs, tuple(ids))
    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    response_json = {"data": ids}
    return response_json


@clerk_card_router.post('/task')
async def create_task(info: AddTask, dbs: AsyncSession = Depends(db_session)):
    """
    创建任务
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('task', f'=="{info.task}"', info.task)
    ]
    result = await TbTask.get_one(dbs, *filter_condition)
    if result:
        raise HTTPException(status_code=403, detail="Duplicate Task.")
    result = await TbTask.add_data(dbs, info)
    response_json = {"data": result}
    return response_json


@clerk_card_router.patch('/task')
async def update_task(info: UpdateTask, dbs: AsyncSession = Depends(db_session)):
    """
    修改任务信息
    :param info:
    :param dbs:
    :return:
    """
    update_data_dict = info.dict(exclude_unset=True)
    filter_condition = [
        ('task', f'=="{info.task}"', info.task)
    ]
    result = await TbTask.get_one(dbs, *filter_condition)
    if result:
        raise HTTPException(status_code=403, detail="Duplicate Task.")
    if len(update_data_dict) > 1:
        result = await TbTask.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="Task does not exist.")
    response_json = {"data": update_data_dict}
    return response_json
