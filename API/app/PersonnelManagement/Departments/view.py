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
    responses={404: {"description": "Not found"}},
    tags=["Departments"])


@departments_router.get('/Department')
async def get_departments(info: SearchDepartment = Depends(SearchDepartment),
                          dbs: AsyncSession = Depends(db_session), ):
    """
        获取部门列表

    :param info:

        需要查询的部门参数，可以根据创建人，部门名称来查询

    :param dbs:

        数据库依赖

    :return:

        包含分页信息的部门列表
    """
    filter_condition = [
        ('department', f'.like(f"%{info.department}%")', info.department),
        ('creator', f'.like(f"%{info.creator}%")', info.creator),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await Departments.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)

    new_result = []
    for res in result:
        new_res = {
            "id": res.id,
            "department": res.department,
            "creator": res.creator,
            "create_time": res.create_time.strftime("%Y-%m-%d")
        }
        new_result.append(new_res)

    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": new_result}
    return response_json


@departments_router.get('/Department/detail')
async def get_departments_one(department_id: Optional[int] = Query(None), dbs: AsyncSession = Depends(db_session)):
    """
        获取某个部门的信息

    :param department_id:

        部门id

    :param dbs:

        数据库依赖

    :return:

        单个部门的信息
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

        部门id

    :param dbs:

        数据库依赖

    :return:

        被删除的部门的id
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

        创建部门所需的参数

    :param dbs:

        数据库依赖

    :return:

        被添加的部门后的id
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

        更新部门信息包含的参数

    :param dbs:

        数据库依赖

    :return:

        更新的部门信息
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
    """
        获取用户  根据部门

    :param dbs:

        数据库依赖

    :param department_id:

        部门id

    :return:

        对应的部门下的用户信息
    """
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
    """
        增加用户关联 根据部门id和用户id

    :param info:

        对应的主表和关联表需要更改的信息

    :param dbs:

        数据库依赖

    :return:

         添加成功的id和已存在的关系的id
    """
    # uid_list, exist_list = await DepartmentUserMapping.filter_add_data_many_(dbs, info.department_id, info.ids)
    uid_list, exist_list = await DepartmentUserMapping.filter_add_data_many(dbs, "department_id", info.department_id,
                                                                            "user_id", info.ids)
    response_json = {"data": uid_list, "exist_data": exist_list}
    return response_json


@departments_router.delete("/DepartmentUserMapping")
async def delete_user_department(info: DepartmentAbout, dbs: AsyncSession = Depends(db_session)):
    """
        删除用户关联 根据部门id和对应的user_id

    :param info:

        department_id和user_id

    :param dbs:

        数据库依赖

    :return:

        返回的被删除的用户信息
    """
    filter_condition = [
        ("department_id", f"=='{info.department_id}'", info.department_id),
        ("user_id", f".in_({info.ids})", info.ids)
    ]
    await DepartmentUserMapping.filter_delete_data(dbs, *filter_condition)
    response_json = {"data": info.ids}
    return response_json


@departments_router.get("/DepartmentRoleMapping")
async def get_department_role(dbs: AsyncSession = Depends(db_session), department_id: int = Query(...)):
    """
        获取角色 根据部门

    :param dbs:

        数据库依赖

    :param department_id:

        部门id

    :return:

        对应部门下的角色信息
    """
    role_list = await Roles.get_role_department(dbs, department_id)
    response_data = []
    for p in role_list:
        p_role = {
            "id": p.id,
            "role": p.role,
            "create_time": p.create_time.strftime("%Y-%m-%d"),
        }
        response_data.append(p_role)
    response_json = {"data": response_data}
    return response_json


@departments_router.post('/DepartmentRoleMapping')
async def add_role_department(info: DepartmentAbout, dbs: AsyncSession = Depends(db_session)):
    """
        增加角色关联 根据部门

    :param info:

        部门id，角色id

    :param dbs:

        数据库依赖

    :return:

        要被新增的数据，已存在的数据
    """
    # uid_list, exist_list = await DepartmentRoleMapping.filter_add_data_many_(dbs, info.department_id, info.ids)
    uid_list, exist_list = await DepartmentRoleMapping.filter_add_data_many(dbs, "department_id", info.department_id,
                                                                            "role_id", info.ids)
    response_json = {"data": uid_list, "exist_data": exist_list}
    return response_json


@departments_router.delete("/DepartmentRoleMapping")
async def delete_role_department(info: DepartmentAbout, dbs: AsyncSession = Depends(db_session)):
    """
        删除角色关联 根据部门

    :param info:

        需要删除的角色id和部门id

    :param dbs:

        数据库依赖

    :return:

        被删除的角色id
    """
    filter_condition = [
        ("department_id", f"=='{info.department_id}'", info.department_id),
        ("role_id", f".in_({info.ids})", info.ids)
    ]
    await DepartmentRoleMapping.filter_delete_data(dbs, *filter_condition)
    response_json = {"data": info.ids}
    return response_json
