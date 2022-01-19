import pandas as pd
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query, HTTPException, Path, UploadFile, File

from sql_models.CardManagement.OrmCardManagement import *
from app.Clerk.Card.DataValidation import *
from sql_models.db_config import db_session

clerk_card_router = APIRouter(
    prefix="/card/v1",
    responses={404: {"card": "Not found"}}, )


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
    创建单条卡号
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


@clerk_card_router.post('/cards')
async def create_cards(infos: List[AddCard], dbs: AsyncSession = Depends(db_session)):
    """
    创建单条或者多条卡号
    :param info:
    :param dbs:
    :return:
    """
    for info in infos:
        filter_condition = [
            ('card_number', f'=="{info.card_number}"', info.card_number)
        ]
        result = await TbCard.get_one(dbs, *filter_condition)
        if result:
            raise HTTPException(status_code=403, detail="Duplicate card.")
    result = await TbCard.add_data_many(dbs, infos)
    response_json = {"data": result}
    return response_json


@clerk_card_router.post('/cards/excel')
async def create_cards_excel(file: UploadFile = File(...), dbs: AsyncSession = Depends(db_session)):
    """
    上传excel文件，使用File类 文件内容会以bytes的形式读入内存 适合于上传小文件
    :param file: 文件
    :param dbs: 数据库
    :return:
    """
    content = await file.read()
    df = pd.read_excel(content)
    header = df.columns.values.tolist()
    set_header = set(header)
    sql_list = []
    if not "面值" in set_header and not "信用卡开卡额度($)" in set_header and not "总余额" in set_header:
        return HTTPException(status_code=501, detail="数据表中没有面值、总余额、信用卡开卡额度($)中的一个")
    if not "平台" in set_header:
        return HTTPException(status_code=501, detail="数据表中缺少字段:平台")
    else:
        platform_ind = header.index("平台")
    if {'名称', '卡号', '过期时间', '安全码', "面值"} <= set_header:
        if not "卡姓名地址" in set_header:
            return HTTPException(status_code=501, detail="数据表中缺少字段:卡姓名地址")
        card_name_ind = header.index("名称")  # 卡名称
        card_number_ind = header.index("卡号")
        valid_period_ind = header.index("过期时间")  # 有效期
        cvv_ind = header.index("安全码")  # cvv
        face_value_ind = header.index("面值")
        name_ind = header.index("卡姓名地址")
        content = df.values
        for i in content:
            filter_condition = [
                ('card_number', f'=="{i[card_number_ind]}"', i[card_number_ind])
            ]
            result = await TbCard.get_one(dbs, *filter_condition)
            if result:
                raise HTTPException(status_code=403, detail="Duplicate card.")
            name = i[name_ind]
            name = name if isinstance(name, str) else ''
            sql_list.append({
                'card_number': i[card_number_ind],
                'face_value': i[face_value_ind],
                'card_name': i[card_name_ind],
                'valid_period': i[valid_period_ind],
                'cvv': str(i[cvv_ind]).zfill(3),
                'platform': i[platform_ind],
                'name': name,
                'card_status': 1
            })
        result = await TbCard.add_data_many(dbs, sql_list)
        response_json = {"data": result}
    elif {'卡号', '状态', "总余额", '拒付率', "有效期", "安全码", "开卡时间", "备注"} <= set_header:
        card_number_ind = header.index("卡号")
        face_value_ind = header.index("总余额")  # 面值
        valid_period_ind = header.index("有效期")
        cvv_ind = header.index("安全码")  # cvv
        zip_ind = ""
        try:
            zip_ind = header.index("zip")
            zip_bool = True
        except:
            zip_bool = False
        note_ind = header.index("备注")
        name_address_ind = ""
        name_ind = ""
        address_ind = ""
        try:
            name_address_ind = header.index("卡姓名地址")  # 卡姓名地址
            name_address_bool = True
        except:
            try:
                name_ind = header.index("Name")  # 卡拥有人名称
                address_ind = header.index("address")  # 地址
                name_address_bool = False
            except:
                return HTTPException(status_code=501, detail="数据表中缺少字段:卡姓名地址")
        content = df.values
        for i in content:
            if zip_bool:
                card_zip = str(i[zip_ind]).zfill(5)
            else:
                card_zip = ""
            if name_address_bool:
                card_name_address = i[name_address_ind]
            else:
                card_name_address = i[name_ind] + " " + i[address_ind] + " " + card_zip
        for i in content:
            filter_condition = [
                ('card_number', f'=="{i[card_number_ind]}"', i[card_number_ind])
            ]
            result = await TbCard.get_one(dbs, *filter_condition)
            if result:
                raise HTTPException(status_code=403, detail="Duplicate card.")
            note = i[note_ind]
            note = note if isinstance(note, str) else ''
            card_name_address = card_name_address if isinstance(card_name_address, str) else ''
            sql_list.append({
                'card_number': i[card_number_ind],
                'face_value': i[face_value_ind],
                'valid_period': i[valid_period_ind],
                'cvv': str(i[cvv_ind]).zfill(3),
                'name': card_name_address,
                # zip=card_zip,
                'note': note,
                'platform': i[platform_ind],
                'card_status': 1
            })
        result = await TbCard.add_data_many(dbs, sql_list)
        response_json = {"data": result}
    elif {'卡ID', '任务ID', "唯一标识", '信用卡卡号', "安全码", "信用卡到期日", "信用卡开卡额度($)", "信用卡余额", "卡段类型",
          "添加时间", "状态", "卡备注"} <= set_header:
        if not "卡姓名地址" in set_header:
            return HTTPException(status_code=501, detail="数据表中缺少字段:卡姓名地址")
        # print("excel3")
        card_number_ind = header.index("信用卡卡号")  # 卡号
        face_value_ind = header.index("信用卡开卡额度($)")  # 面值
        valid_period_ind = header.index("信用卡到期日")  # 有效期
        cvv_ind = header.index("安全码")  # cvv
        note_ind = header.index("卡备注")  # 备注
        name_address_ind = header.index("卡姓名地址")  # 卡姓名地址
        content = df.values
        for i in content:
            filter_condition = [
                ('card_number', f'=="{i[card_number_ind]}"', i[card_number_ind])
            ]
            result = await TbCard.get_one(dbs, *filter_condition)
            if result:
                raise HTTPException(status_code=403, detail="Duplicate card.")
            note = i[note_ind]
            note = note if isinstance(note, str) else ''
            name = i[name_address_ind]
            name = name if isinstance(name, str) else ''
            sql_list.append({
                'card_number': i[card_number_ind],
                'face_value': i[face_value_ind],
                'valid_period': i[valid_period_ind],
                'cvv': str(i[cvv_ind]).zfill(3),
                'note': note,
                'platform': i[platform_ind],
                'name': name,
                'card_status': 1
            })
        result = await TbCard.add_data_many(dbs, sql_list)
        response_json = {"data": result}
    else:
        return HTTPException(status_code=501, detail="数据表中没有面值、总余额、信用卡开卡额度($)中的一个")
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
