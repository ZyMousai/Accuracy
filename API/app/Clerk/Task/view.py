# Departments 视图
from sql_models.CardManagement.OrmCardManagement import TbTask
from app.Clerk.Task.DataValidation import AddTask, UpdateTask, SearchTask
from sqlalchemy.ext.asyncio import AsyncSession
from sql_models.db_config import db_session
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from typing import Optional, List

clerk_task_router = APIRouter(
    prefix="/task/v1",
    responses={404: {"task": "Not found"}}, )


@clerk_task_router.get('/')
async def get_task(info: SearchTask = Depends(SearchTask), dbs: AsyncSession = Depends(db_session), ):
    """
    获取任务列表
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('task', f'.like(f"%{info.task}%")', info.task),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await TbTask.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@clerk_task_router.get('/{task_id}')
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


@clerk_task_router.delete('/')
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


@clerk_task_router.post('/')
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


@clerk_task_router.patch('/')
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
