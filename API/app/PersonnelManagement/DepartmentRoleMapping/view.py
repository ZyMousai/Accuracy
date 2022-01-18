# Departments 视图
from sql_models.PersonnelManagement.OrmPersonnelManagement import DepartmentRoleMapping
from app.PersonnelManagement.DepartmentRoleMapping.DataValidation import AddDepartmentRoleMapping, \
    UpdateDepartmentRoleMapping, SearchDepartmentRoleMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sql_models.db_config import db_session
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List

departments_role_mapping_router = APIRouter(
    prefix="/departments_role_mapping/v1",
    responses={404: {"description": "Not found"}}, )


@departments_role_mapping_router.get('/')
async def get_departments_role_mapping(info: SearchDepartmentRoleMapping = Depends(SearchDepartmentRoleMapping),
                          dbs: AsyncSession = Depends(db_session), ):
    """
    获取部门角色映射
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('department_id', f'=={info.department_id}', info.department_id),
        ('role_id', f'=={info.role_id}', info.role_id),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await DepartmentRoleMapping.get_all_detail_page(dbs, info.page, info.page_size,
                                                                                *filter_condition)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": result}
    return response_json


@departments_role_mapping_router.get('/{drm_id}')
async def get_departments_role_mapping_one(drm_id: Optional[int] = Query(None), dbs: AsyncSession = Depends(db_session)):
    """
    获取某个部门角色映射的信息
    :param drm_id:
    :param dbs:
    :return:
    """
    result = await DepartmentRoleMapping.get_one_detail(dbs, drm_id)
    if not result:
        raise HTTPException(status_code=404, detail="Get non-existent resources.")
    response_json = {"data": result}
    return response_json


@departments_role_mapping_router.delete('/')
async def delete_departments_role_mapping(ids: Optional[List[int]] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
    删除部门角色映射 可批量
    :param ids:
    :param dbs:
    :return:
    """
    # 真实删除部门角色映射表
    await DepartmentRoleMapping.delete_data(dbs, tuple(ids))
    response_json = {"data": ids}
    return response_json


@departments_role_mapping_router.post('/')
async def create_departments_role_mapping(drm_id: AddDepartmentRoleMapping, dbs: AsyncSession = Depends(db_session)):
    """
    创建部门角色映射
    :param drm_id:
    :param dbs:
    :return:
    """
    result = await DepartmentRoleMapping.add_data(dbs, drm_id)
    if not result:
        raise HTTPException(status_code=403, detail="Duplicate account.")
    response_json = {"data": result}
    return response_json


@departments_role_mapping_router.patch('/')
async def update_departments_role_mapping(drm_id: UpdateDepartmentRoleMapping, dbs: AsyncSession = Depends(db_session)):
    """
    修改部门角色映射信息
    :param drm_id:
    :param dbs:
    :return:
    """
    update_data_dict = drm_id.dict(exclude_unset=True)
    if len(update_data_dict) > 1:
        result = await DepartmentRoleMapping.update_data(dbs, update_data_dict, is_delete=0)
        if not result:
            raise HTTPException(status_code=403, detail="role does not exist.")
    response_json = {"data": update_data_dict}
    return response_json
