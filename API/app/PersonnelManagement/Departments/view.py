# Departments 视图
from sql_models.PersonnelManagement.OrmPersonnelManagement import Departments, DepartmentRoleMapping, \
    DepartmentUserMapping, Users, Roles
from app.PersonnelManagement.Departments.DataValidation import AddDepartments, UpdateDepartment, SearchDepartment, \
    DepartmentAbout, DepartmentGet
from sqlalchemy.ext.asyncio import AsyncSession
from sql_models.db_config import db_session
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List

departments_router = APIRouter(
    prefix="/departments/v1",
    responses={404: {"description": "Not found"}}, )


@departments_router.get('/Department')
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


@departments_router.get('/Department/{department_id}')
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


@departments_router.delete('/Department')
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


@departments_router.post('/Department')
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


@departments_router.patch('/Department')
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


@departments_router.get("/DepartmentUserMapping")
async def get_department_user(dbs: AsyncSession = Depends(db_session), department_id: int = Query(...)):
    """获取用户  根据部门 """
    user_list = await Users.get_user_department(dbs, department_id)
    response_data = []
    for p in user_list:
        p_user = {
            "id": p.id,
            "account": p.account,
            "name": p.name,
            "entry_time": p.entry_time,
        }
        response_data.append(p_user)
    response_json = {"data": response_data}
    return response_json


@departments_router.post('/DepartmentUserMapping')
async def add_user_department(info: DepartmentAbout, dbs: AsyncSession = Depends(db_session)):
    """增加用户关联 根据部门"""
    uid_list, exist_list = await DepartmentUserMapping.filter_add_data_many_(dbs, info.department_id, info.ids)
    response_json = {"data": uid_list, "exist_data": exist_list}
    return response_json


@departments_router.delete("/DepartmentUserMapping")
async def delete_user_department(info: DepartmentAbout, dbs: AsyncSession = Depends(db_session)):
    """删除用户关联 根据部门"""
    filter_condition = [
        ("department_id", f"=='{info.department_id}'", info.department_id),
        ("user_id", f".in_({info.ids})", info.ids)
    ]
    await DepartmentUserMapping.filter_delete_data(dbs, *filter_condition)
    response_json = {"data": info.ids}
    return response_json


@departments_router.get("/DepartmentRoleMapping")
async def get_department_role(dbs: AsyncSession = Depends(db_session), department_id: int = Query(...)):
    """获取角色 根据部门 """
    role_list = await Roles.get_role_department(dbs, department_id)
    response_data = []
    for p in role_list:
        p_role = {
            "id": p.id,
            "role": p.role,
            "create_time": p.create_time,
        }
        response_data.append(p_role)
    response_json = {"data": response_data}
    return response_json


@departments_router.post('/DepartmentRoleMapping')
async def add_role_department(info: DepartmentAbout, dbs: AsyncSession = Depends(db_session)):
    """增加角色关联 根据部门"""
    uid_list, exist_list = await DepartmentRoleMapping.filter_add_data_many_(dbs, info.department_id, info.ids)
    response_json = {"data": uid_list, "exist_data": exist_list}
    return response_json


@departments_router.delete("/DepartmentRoleMapping")
async def delete_role_department(info: DepartmentAbout, dbs: AsyncSession = Depends(db_session)):
    """删除角色关联 根据部门"""
    filter_condition = [
        ("department_id", f"=='{info.department_id}'", info.department_id),
        ("role_id", f".in_({info.ids})", info.ids)
    ]
    await DepartmentRoleMapping.filter_delete_data(dbs, *filter_condition)
    response_json = {"data": info.ids}
    return response_json
