# Departments 视图
from sql_models.PersonnelManagement.OrmPersonnelManagement import Departments, DepartmentRoleMapping, \
    DepartmentUserMapping
from app.PersonnelManagement.Departments.DataValidation import AddDepartments, UpdateDepartment, SearchDepartment
from sqlalchemy.ext.asyncio import AsyncSession
from sql_models.db_config import db_session
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List

departments_router = APIRouter(
    prefix="/departments/v1",
    responses={404: {"description": "Not found"}}, )


@departments_router.get('/')
async def get_departments(info: SearchDepartment = Depends(SearchDepartment),
                          dbs: AsyncSession = Depends(db_session), ):
    """
    获取部门列表
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('department', f'.like(f"%{info.department}%")', info.department),
        ('creator', f'.like(f"%{info.creator}%")', info.creator),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await Departments.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@departments_router.get('/{department_id}')
async def get_departments_one(department_id: Optional[int] = Query(None), dbs: AsyncSession = Depends(db_session)):
    """
    获取某个部门的信息
    :param department_id:
    :param dbs:
    :return:
    """
    result = await Departments.get_one_detail(dbs, department_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


@departments_router.delete('/')
async def delete_departments(ids: Optional[List[int]] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
    删除部门 可批量
    :param ids:
    :param dbs:
    :return:
    """
    # 真实删除部门表
    await Departments.delete_data(dbs, tuple(ids))
    # 删除菜单关联 根据role
    filter_condition = [
        ("department_id", f".in_({ids})", ids)
    ]
    await DepartmentRoleMapping.filter_delete_data(dbs, *filter_condition)
    await DepartmentUserMapping.filter_delete_data(dbs, *filter_condition)

    response_json = {"data": ids}
    return response_json


@departments_router.post('/')
async def create_departments(department_id: AddDepartments, dbs: AsyncSession = Depends(db_session)):
    """
    创建部门
    :param department_id:
    :param dbs:
    :return:
    """
    result = await Departments.add_data(dbs, department_id)
    if not result:
        raise HTTPException(status_code=403, detail="Duplicate account.")
    response_json = {"data": result}
    return response_json


@departments_router.patch('/')
async def update_departments(department_id: UpdateDepartment, dbs: AsyncSession = Depends(db_session)):
    """
    修改部门信息
    :param department_id:
    :param dbs:
    :return:
    """
    update_data_dict = department_id.dict(exclude_unset=True)
    if len(update_data_dict) > 1:
        result = await Departments.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="User does not exist.")
    response_json = {"data": update_data_dict}
    return response_json
