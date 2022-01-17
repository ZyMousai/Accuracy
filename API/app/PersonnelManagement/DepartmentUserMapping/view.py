# Departments 视图
from sql_models.PersonnelManagement.OrmPersonnelManagement import DepartmentUserMapping
from app.PersonnelManagement.DepartmentUserMapping.DataValidation import AddDepartmentUserMapping, \
    UpdateDepartmentUserMapping, SearchDepartmentUserMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sql_models.db_config import db_session
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List

departments_user_mapping_router = APIRouter(
    prefix="/departments_user_mapping/v1",
    responses={404: {"description": "Not found"}}, )


@departments_user_mapping_router.get('/')
async def get_departments_user_mapping(info: SearchDepartmentUserMapping = Depends(SearchDepartmentUserMapping),
                          dbs: AsyncSession = Depends(db_session), ):
    """
    获取部门用户映射
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('department_id', f'=={info.department_id}', info.department_id),
        ('user_id', f'=={info.user_id}', info.user_id),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await DepartmentUserMapping.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@departments_user_mapping_router.get('/{dum_id}')
async def get_departments_user_mapping_one(dum_id: Optional[int] = Query(None), dbs: AsyncSession = Depends(db_session)):
    """
    获取某个部门用户映射的信息
    :param dum_id:
    :param dbs:
    :return:
    """
    result = await DepartmentUserMapping.get_one_detail(dbs, dum_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


@departments_user_mapping_router.delete('/')
async def delete_departments_user_mapping(ids: Optional[List[int]] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
    删除部门用户映射 可批量
    :param ids:
    :param dbs:
    :return:
    """
    # 真实删除部门用户映射表
    await DepartmentUserMapping.delete_data(dbs, tuple(ids))
    response_json = {"data": ids}
    return response_json


@departments_user_mapping_router.post('/')
async def create_departments_user_mapping(dum_id: AddDepartmentUserMapping, dbs: AsyncSession = Depends(db_session)):
    """
    创建部门用户映射
    :param dum_id:
    :param dbs:
    :return:
    """
    result = await DepartmentUserMapping.add_data(dbs, dum_id)
    if not result:
        raise HTTPException(status_code=403, detail="Duplicate account.")
    response_json = {"data": result}
    return response_json


@departments_user_mapping_router.patch('/')
async def update_departments_user_mapping(dum_id: UpdateDepartmentUserMapping, dbs: AsyncSession = Depends(db_session)):
    """
    修改部门用户映射信息
    :param dum_id:
    :param dbs:
    :return:
    """
    update_data_dict = dum_id.dict(exclude_unset=True)
    if len(update_data_dict) > 1:
        result = await DepartmentUserMapping.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="User does not exist.")
    response_json = {"data": update_data_dict}
    return response_json
