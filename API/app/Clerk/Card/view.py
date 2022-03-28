# 文员卡号，联盟，任务，账号视图
import pandas as pd
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, File

from sql_models.Clerk.OrmCardManagement import *
from app.Clerk.Card.DataValidation import *
from sql_models.db_config import db_session

clerk_card_router = APIRouter(
    prefix="/card/v1",
    responses={404: {"card": "Not found"}},
    tags=["Card"]
)


@clerk_card_router.get('/card')
async def get_card(info: SearchCard = Depends(SearchCard), dbs: AsyncSession = Depends(db_session), ):
    """
        获取卡号列表，对应卡号绑定的任务，根据传递的参数来决定列表内容，逻辑较多，重新构建两次字典，绑定的任务通过构建卡号字典的task_set字段展示出来
    param info:

        查询的条件，作为依赖项目，根据依赖来决定是否必传

    param dbs:

        数据库依赖

    return:

        卡号信息，余额(由绑定的任务而产生)，卡号对应绑定的任务

    """
    filter_condition = [
        ('card_number', f'.like("%{info.card_number}%")', info.card_number),
        ('platform', f'.like("%{info.platform}%")', info.platform),
        ('is_delete', '==0', 0),
        ('retain', f'=={info.retain}', info.retain),
        ('card_status', f'=={info.card_status}', info.card_status),
    ]
    result, count, total_page = await TbCard.get_all_detail_page_desc(dbs, info.page, info.page_size, *filter_condition)

    # 获取所有卡id
    all_card_id = []
    for res in result:
        all_card_id.append(res.id)
    # 获取对应卡id的所有任务
    filter_condition = [
        ('card_id', f'.in_(' + str(all_card_id) + ')', all_card_id),
        ('is_delete', '==0', 0)
    ]
    task_result = await TbTask.get_all(dbs, *filter_condition)

    # 把获取到的任务以卡id为key建立dict
    task_dict = {}
    for task in task_result:
        # 获取对应每个任务的
        task_card_id = task.card_id
        # 通过task.account_id获取uid的逻辑
        args = [
            ('id', f'=={task.account_id}', task.account_id),
            ('is_delete', '==0', 0),
        ]
        account_res = await TbAccount.get_one(dbs, *args)
        new_task_dict = {
            "id": task.id,
            "uid": account_res.uid,
            # "alliance_id": task.account_id,
            "user": task.user,
            "is_delete": task.is_delete,
            "task": task.task,
            "consume": task.consume,
            "card_id": task.card_id,
            "commission": task.commission,
            "secondary_consumption": task.secondary_consumption,
            "account_id": task.account_id,
            "creation_date": task.creation_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        if task.card_id not in task_dict.keys():
            task_dict[task_card_id] = [new_task_dict]
        else:
            task_dict[task_card_id].append(new_task_dict)
    # 对卡数据进行重新归纳赋值
    new_result = []
    task_di_keys = task_dict.keys()
    for res in result:
        res_id = res.id
        new_res = {
            "id": res_id,
            "card_number": res.card_number,
            "face_value": res.face_value,
            "valid_period": res.valid_period,
            "cvv": res.cvv,
            "card_status": res.card_status,
            "name": res.name,
            "platform": res.platform,
            "note": res.note,
            "card_name": res.card_name,
            "create_time": res.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            "retain": res.retain,
        }
        # 定义额外的任务的参数
        if res_id in task_di_keys:
            new_res["task_set"] = task_dict[res_id]
        else:
            new_res["task_set"] = []
        new_result.append(new_res)
        # 添加余额的逻辑
        total_consume = 0
        # 如果对应的卡有任务的话，进行每个任务的余额遍历和添加
        if new_res["task_set"]:
            for single_task in task_dict[res_id]:
                total_consume += single_task['consume']
        balance = res.face_value - total_consume
        new_res['balance'] = balance
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": new_result}
    return response_json


@clerk_card_router.get('/card/detail')
async def get_card_one(card_id: int = Query(..., title='卡号id', description="卡号id", ge=1),
                       dbs: AsyncSession = Depends(db_session)):
    """
        单独一张卡的信息，不包含绑定的任务
    param card_id:

        卡号的id

    param dbs:

        数据库依赖

    return:

        单独一张卡的信息，不包含绑定的任务

    """
    result = await TbCard.get_one_detail(dbs, card_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


@clerk_card_router.post('/card')
async def create_card(info: AddCard, dbs: AsyncSession = Depends(db_session)):
    """
        创建单独的一张卡
    param info:

        对应的卡号的信息，依赖给的不是必传，但逻辑上是每个字段都要传

    param dbs:

        数据库依赖

    return:

        创建单独的一张卡

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


@clerk_card_router.delete('/card')
async def delete_card(ids: List[int] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
        逻辑删除一张卡，后续需要改成真实删除，记得改！目前未改！
    param ids:

        卡号的id

    param dbs:

        数据库依赖

    return:

        逻辑删除一张卡

    """
    result = await TbCard.delete_data_logic(dbs, tuple(ids))
    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    response_json = {"data": ids}
    return response_json


@clerk_card_router.post('/cards')
async def create_cards(information: List[AddCard], dbs: AsyncSession = Depends(db_session)):
    """
        创建单独的一张卡或者多张卡
    param info:

        对应的卡号的信息，依赖给的不是必传，但逻辑上是每个字段都要传

    param dbs:

        数据库依赖

    return:

        创建单独的一张卡或者多张卡

    """
    for info in information:
        filter_condition = [
            ('card_number', f'=="{info.card_number}"', info.card_number)
        ]
        result = await TbCard.get_one(dbs, *filter_condition)
        if result:
            raise HTTPException(status_code=403, detail="Duplicate card.")
    result = await TbCard.add_data_many(dbs, information)
    response_json = {"data": result}
    return response_json


@clerk_card_router.post('/cards/excel')
async def create_cards_excel(file: UploadFile = File(...), dbs: AsyncSession = Depends(db_session)):
    """
        上传excel文件，使用File类 文件内容会以bytes的形式读入内存 适合于上传小文件

    param file:

        文件
    param dbs:

        数据库
    return:

        针对不同情况的返回状态和信息提示
    """
    content = await file.read()
    df = pd.read_excel(content)
    header = df.columns.values.tolist()
    set_header = set(header)
    sql_list = []
    if "面值" not in set_header and "信用卡开卡额度($)" not in set_header and "总余额" not in set_header:
        return HTTPException(status_code=501, detail="数据表中没有面值、总余额、信用卡开卡额度($)中的一个")
    if "平台" not in set_header:
        return HTTPException(status_code=501, detail="数据表中缺少字段:平台")
    else:
        platform_ind = header.index("平台")
    if {'名称', '卡号', '过期时间', '安全码', "面值"} <= set_header:
        if "卡姓名地址" not in set_header:
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
        # noinspection PyBroadException
        try:
            zip_ind = header.index("zip")
            zip_bool = True
        except Exception:
            zip_bool = False
        note_ind = header.index("备注")
        name_address_ind = ""
        name_ind = ""
        address_ind = ""
        # noinspection PyBroadException
        try:
            name_address_ind = header.index("卡姓名地址")  # 卡姓名地址
            name_address_bool = True
        except Exception:
            # noinspection PyBroadException
            try:
                name_ind = header.index("Name")  # 卡拥有人名称
                address_ind = header.index("address")  # 地址
                name_address_bool = False
            except Exception:
                return HTTPException(status_code=501, detail="数据表中缺少字段:卡姓名地址")
        content = df.values
        card_name_address = ""
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
        if "卡姓名地址" not in set_header:
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
        更新卡号信息
    param info:

        对应的卡号的信息，依赖给的不是必传，但逻辑上是每个字段都要传，id必传

    param dbs:

        数据库依赖

    return:

        更新卡号信息

    """
    update_data_dict = info.dict(exclude_unset=True)
    # filter_condition = [
    #     ('card_number', f'=="{info.card_number}"', info.card_number)
    # ]
    # result = await TbCard.get_one(dbs, *filter_condition)
    # if result:
    #     raise HTTPException(status_code=403, detail="Duplicate card.")
    if len(update_data_dict) > 1:
        result = await TbCard.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="card does not exist.")
    response_json = {"data": update_data_dict}
    return response_json


@clerk_card_router.get('/account')
async def get_account(info: SearchAccount = Depends(SearchAccount), dbs: AsyncSession = Depends(db_session), ):
    """
        获取账号信息
    param info:

        对应的账号信息，参数不是必传

    param dbs:

        数据库依赖

    return:

        获取账号信息，包含了分页

    """
    filter_condition = [
        # ('account_name', f'.like("%{info.account_name}%")', info.account_name),
        ('uid', f'.like("%{info.uid}%")', info.uid),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await TbAccount.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@clerk_card_router.get('/account/detail')
async def get_account_one(account_id: int = Query(..., title='账号id', description="账号id", ge=1),
                          dbs: AsyncSession = Depends(db_session)):
    """
        获取某个账号信息
    param account_id:

        账号的id

    param dbs:

        数据库依赖

    return:

        获取某个账号信息

    """
    result = await TbAccount.get_one_detail(dbs, account_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


@clerk_card_router.delete('/account')
async def delete_account(ids: List[int] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
        逻辑删除账号信息，后续需要改成真实删除
    param ids:

        需要删除的账号列表，元素是id

    param dbs:

        数据库依赖

    return:

        被逻辑删除的账号的id

    """
    result = await TbAccount.delete_data_logic(dbs, tuple(ids))
    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    response_json = {"data": ids}
    return response_json


@clerk_card_router.post('/account')
async def create_account(user: AddAccount, dbs: AsyncSession = Depends(db_session)):
    """
        创建单个账户，账户实际是uid，要和id区分开，id是自增的主键
    param user:

        需要创建的用户的字段值

    param dbs:

        数据库依赖

    return:

        创建的单个用户的信息

    """
    filter_condition = [
        ('uid', f'=="{user.uid}"', user.uid),
        # ('uid', f'=="{user.uid}"', user.uid),
    ]
    # create_account_query = f"or_(cls.account_name=='{user.account_name}',cls.uid=='{user.uid}')"
    # filter_condition = [
    #     create_account_query
    # ]
    result = await TbAccount.get_one(dbs, *filter_condition)
    if result:
        # raise HTTPException(status_code=403, detail="Duplicate account.")
        return {"data": result.id}
    result = await TbAccount.add_data(dbs, user)
    response_json = {"data": result}
    return response_json


@clerk_card_router.patch('/account')
async def update_account(user: UpdateAccount, dbs: AsyncSession = Depends(db_session)):
    """
        更新账户信息
    param user:

        需要更新的账户信息

    param dbs:

        数据库依赖

    return:

        更新后的账户的值

    """
    update_data_dict = user.dict(exclude_unset=True)
    # filter_condition = [
    #     ('account_name', f'=="{user.account_name}"', user.account_name)
    # ]
    # result = await TbAccount.get_one(dbs, *filter_condition)
    # if result:
    #     raise HTTPException(status_code=403, detail="Duplicate account.")
    if len(update_data_dict) > 1:
        result = await TbAccount.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="User does not exist.")
    response_json = {"data": update_data_dict}
    return response_json


# @clerk_card_router.get('/alliance')
# async def get_alliance(info: SearchAlliance = Depends(SearchAlliance), dbs: AsyncSession = Depends(db_session), ):
#     """
#     获取联盟列表
#     :param info:
#     :param dbs:
#     :return:
#     """
#     filter_condition = [
#         ('alliance_name', f'.like("%{info.alliance_name}%")', info.alliance_name),
#         ('is_delete', '==0', 0)
#     ]
#     result, count, total_page = await TbAlliance.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
#     response_json = {"total": count,
#                      "page": info.page,
#                      "page_size": info.page_size,
#                      "total_page": total_page,
#                      "data": result}
#     return response_json
#
#
# @clerk_card_router.get('/alliance/{alliance_id}')
# async def get_alliance_one(alliance_id: int = Path(..., title='联盟id', description="联盟id", ge=1),
#                            dbs: AsyncSession = Depends(db_session)):
#     """
#     获取某个联盟的信息
#     :param alliance_id:
#     :param dbs:
#     :return:
#     """
#     result = await TbAlliance.get_one_detail(dbs, alliance_id)
#     if not result:
#         raise HTTPException(status_code=404, detail="Get non-existent resources.")
#     response_json = {"data": result}
#     return response_json
#
#
# @clerk_card_router.delete('/alliance')
# async def delete_alliance(ids: List[int] = Query(...), dbs: AsyncSession = Depends(db_session)):
#     """
#     删除联盟 可批量
#     :param ids:
#     :param dbs:
#     :return:
#     """
#     result = await TbAlliance.delete_data_logic(dbs, tuple(ids))
#     if not result:
#         raise HTTPException(status_code=404, detail="Delete non-existent resources.")
#     response_json = {"data": ids}
#     return response_json
#
#
# @clerk_card_router.post('/alliance')
# async def create_alliance(info: AddAlliance, dbs: AsyncSession = Depends(db_session)):
#     """
#     创建联盟
#     :param info:
#     :param dbs:
#     :return:
#     """
#     filter_condition = [
#         ('alliance_name', f'=="{info.alliance_name}"', info.alliance_name)
#     ]
#     result = await TbAlliance.get_one(dbs, *filter_condition)
#     if result:
#         raise HTTPException(status_code=403, detail="Duplicate alliance.")
#     result = await TbAlliance.add_data(dbs, info)
#     response_json = {"data": result}
#     return response_json
#
#
# @clerk_card_router.patch('/alliance')
# async def update_alliance(info: UpdateAlliance, dbs: AsyncSession = Depends(db_session)):
#     """
#     修改联盟信息
#     :param info:
#     :param dbs:
#     :return:
#     """
#     update_data_dict = info.dict(exclude_unset=True)
#     filter_condition = [
#         ('alliance_name', f'=="{info.alliance_name}"', info.alliance_name)
#     ]
#     result = await TbAlliance.get_one(dbs, *filter_condition)
#     if result:
#         raise HTTPException(status_code=403, detail="Duplicate alliance.")
#     if len(update_data_dict) > 1:
#         result = await TbAlliance.update_data(dbs, update_data_dict, is_delete=0)
#         if not result:
#             raise HTTPException(status_code=403, detail="alliance does not exist.")
#     response_json = {"data": update_data_dict}
#     return response_json


@clerk_card_router.get('/task')
async def get_task(info: SearchTask = Depends(SearchTask), dbs: AsyncSession = Depends(db_session)):
    """
        获取任务信息列表，这里把通用方法重写了一遍，因为获取的值有一定的差异
    param info:

        对应的任务信息，参数不是必传

    param dbs:

        数据库依赖

    return:

        获取任务信息，包含了分页

    """
    args = [
        ('account_id', f'=="{info.account_id}"', info.account_id),
        ('task', f'.like("%{info.task}%")', info.task),
        ('is_delete', '==0', 0),
    ]
    print(info.account_id)
    filter_condition = list()
    for x in args:
        if x[2] is not None:
            filter_condition.append(eval(f'TbTask.{x[0]}{x[1]}'))
    # 处理分页
    count = await TbTask.get_data_count(dbs, *filter_condition)
    remainder = count % info.page_size
    if remainder == 0:
        total_page = int(count // info.page_size)
    else:
        total_page = int(count // info.page_size) + 1

    # 查询数据
    # scalars主要作用是把数据映射到orm类上去，不然得到的就是一行一行的查询结果
    _orm = select(
        TbTask.id,
        TbTask.is_delete,
        TbTask.card_id,
        TbTask.account_id,
        TbTask.creation_date,
        TbTask.commission,
        TbTask.user,
        TbTask.note,
        # TbTask.alliance_id,
        TbTask.task,
        TbTask.consume,
        TbTask.secondary_consumption,
        TbAccount.uid,
        # TbAccount.account_name,
    ).where(*filter_condition).join(TbTask.account).order_by().limit(info.page_size) \
        .offset((info.page - 1) * info.page_size)
    result = (await dbs.execute(_orm)).all()
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@clerk_card_router.get('/account_task_name')
async def get_task(info: SearchTask = Depends(SearchTask), dbs: AsyncSession = Depends(db_session)):
    """
        获取匹配的uuid的任务名
    param info:

        对应的任务信息，参数不是必传

    param dbs:

        数据库依赖

    return:

        获取任务信息，包含了分页

    """
    args = [
        ('account_id', f'=="{info.account_id}"', info.account_id),
        ('is_delete', '==0', 0),
    ]
    print(info.account_id)
    result = await TbTask.get_one(dbs, *args)
    print(result)
    response_json = {"data": result}
    return response_json


# @clerk_card_router.get('/task')
# async def get_task(info: SearchTask = Depends(SearchTask), dbs: AsyncSession = Depends(db_session), ):
#     """
#     获取任务列表
#     :param info:
#     :param dbs:
#     :return:
#     """
#     filter_condition = [
#         ('task', f'.like("%{info.task}%")', info.task),
#         ('is_delete', '==0', 0)
#     ]
#     result, count, total_page = await TbTask.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
#     response_json = {"total": count,
#                      "page": info.page,
#                      "page_size": info.page_size,
#                      "total_page": total_page,
#                      "data": result}
#     return response_json


@clerk_card_router.get('/task/detail')
async def get_task_one(task_id: int = Query(..., title='任务id', description="任务id", ge=1),
                       dbs: AsyncSession = Depends(db_session)):
    """
        获取某个任务信息
    param task_id:

        任务的id

    param dbs:

        数据库依赖

    return:

        获取某个任务信息

    """
    result = await TbTask.get_one_detail(dbs, task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


@clerk_card_router.delete('/task')
async def delete_task(ids: List[int] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
        逻辑删除任务信息，后续需要改成真实删除
    param ids:

        需要删除的账号列表，元素是id

    param dbs:

        数据库依赖

    return:

        被逻辑删除的任务的id

    """
    result = await TbTask.delete_data_logic(dbs, tuple(ids))
    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    response_json = {"data": ids}
    return response_json


@clerk_card_router.post('/task')
async def create_task(info: AddTask, dbs: AsyncSession = Depends(db_session)):
    """
        创建任务，任务名可以重复，只要绑定对应的Account_id就可以，Account表对应的是uuid
    param info:

        对应的需要新增的任务字段，有些必传

    param dbs:

        数据库依赖

    return:

        创建后的任务的任务信息

    """
    # filter_condition = [
    #     ('task', f'=="{info.task}"', info.task)
    # ]
    # result = await TbTask.get_one(dbs, *filter_condition)
    # if result:
    #     raise HTTPException(status_code=403, detail="Duplicate Task.")
    result = await TbTask.add_data(dbs, info)
    response_json = {"data": result}
    return response_json


@clerk_card_router.patch('/task')
async def update_task(info: UpdateTask, dbs: AsyncSession = Depends(db_session)):
    """
        修改任务信息
    param info:

        对应的需要修改的任务字段

    param dbs:

        数据库依赖

    return:

        更新后的任务的任务信息

    """
    update_data_dict = info.dict(exclude_unset=True)
    # filter_condition = [
    #     ('task', f'=="{info.task}"', info.task)
    # ]
    # result = await TbTask.get_one(dbs, *filter_condition)
    # if result:
    #     raise HTTPException(status_code=403, detail="Duplicate Task.")
    if len(update_data_dict) > 1:
        result = await TbTask.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="Task does not exist.")
    response_json = {"data": update_data_dict}
    return response_json


@clerk_card_router.get('/statistics')
async def get_statistics(info: Statistics = Depends(Statistics),
        # uid: str = Query(..., title="uid值", description="需要通过uid来查询account和task关联数据的消耗额和收益"),
        # start_time: str = Query(..., title="开始时间", description="需要通过uid来查询account和task关联数据的消耗额和收益"),
        # end_time: str = Query(..., title="结束时间", description="需要通过uid来查询account和task关联数据的消耗额和收益"),
                         dbs: AsyncSession = Depends(db_session)):
    """
        统计对应的uid的消耗金额数量，收益总量
    param uid:

        tb_Account表的uid值，是对应着每个任务，任务在创建的时候名字可以重复，但是uid不重复

    param dbs:

        数据库依赖

    return:

        uid对应的所有消耗额和收益

    """
    # print(info.uid)
    filter_condition = [
        ('uid', f'=="{info.uid}"', info.uid),
        ('is_delete', '==0', 0)
    ]
    single_account = await TbAccount.get_one(dbs, *filter_condition)
    if single_account:
        # 获得uid对应的account_id,用于在tb_Task表里查询消耗额
        account_id = single_account.id
    else:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    filter_condition = [
        ("creation_date", f'>="{info.start_time}"', info.start_time),
        ("creation_date", f'<="{info.end_time}"', info.end_time)
    ]
    consume_commission_list = await TbTask.get_task_account_consume_commission(dbs, account_id, filter_condition)
    total_consume = 0
    total_commission = 0
    for consume_commission in consume_commission_list:
        total_consume += consume_commission['consume']
        total_commission += consume_commission['commission']
    return {
        "total_consume": total_consume,
        "total_commission": total_commission,
    }
