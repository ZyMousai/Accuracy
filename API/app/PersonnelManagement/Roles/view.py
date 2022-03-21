# Roles 视图
from typing import Optional, List

from fastapi import APIRouter, Depends, Request, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.PersonnelManagement.Roles.DataValidation import SearchRole, AddRole, UpdateRole, RoleAbout
from sql_models.PersonnelManagement.OrmPersonnelManagement import Roles, Menu, RoleMenuMapping, DepartmentRoleMapping, \
    RoleUserMapping, RolePermissionMapping, RoleAccountMapping, Permission
from sql_models.db_config import db_session

roles_router = APIRouter(
    prefix="/roles/v1",
    responses={404: {"description": "Not found"}},
    tags=["Roles"])


def get_role_id(request: Request):
    return request.state.role_id
    # return 1
    # return 4


operate_dict = {
    1: "新增",
    2: "修改",
    3: "查看",
    4: "删除",
}


@roles_router.get("/RoleMenu")
async def get_role_menu(dbs: AsyncSession = Depends(db_session), role_id=Depends(get_role_id)):
    """
        获取菜单 根据role

    :param dbs:

        数据库依赖

    :param role_id:

        登录用户的角色id

    :return:

         对应的角色菜单
    """
    # 通过role_menu_mapping去查询menu_id，给对应的menu_id赋值

    # 根据role获取菜单
    menu_list = await Menu.get_menu_role(dbs, role_id)

    filter_condition = [
        ('role_id', f'=={role_id}', role_id),
        ('is_delete', '==0', 0)
    ]
    results = await RolePermissionMapping.get_all(dbs, *filter_condition)

    menu_permission = await Permission.get_all(dbs, *[('is_delete', '==0', 0)])

    result_menu_hash = {menu.id: menu for menu in await Menu.get_all(dbs, *[('is_delete', '==0', 0)])}

    parent_menu_ids = [menu.id for menu in await Menu.get_all(dbs, *[('is_delete', '==0', 0)]) if menu.pid == 0]

    response_data = []
    for parent_id in parent_menu_ids:
        p_menu = {
            "id": result_menu_hash[parent_id].id,
            "pid": result_menu_hash[parent_id].pid,
            "name": result_menu_hash[parent_id].menu_name,
            "path": result_menu_hash[parent_id].menu_path,
            "children": list()
        }
        for children_menu in menu_list:
            if children_menu.pid == parent_id:
                s_menu = {
                    "id": children_menu.id,
                    "pid": children_menu.pid,
                    "name": children_menu.menu_name,
                    "path": children_menu.menu_path,
                    "permission": list()
                }
                for menu_permission_item in menu_permission:
                    if menu_permission_item.menu_id == children_menu.id:
                        permission = {
                            "id": menu_permission_item.id,
                            "p_method": menu_permission_item.p_method,
                            "operate": operate_dict[menu_permission_item.operate],
                            "menu_id": menu_permission_item.menu_id,
                            "remark": menu_permission_item.remark
                        }
                        s_menu.get('permission').append(permission)
                p_menu.get("children").append(s_menu)
        p_menu['children'] = sorted(p_menu['children'], key=lambda x: x['id'])
        if p_menu['children']:
            response_data.append(p_menu)

    # response_data = []
    # for p in menu_list:
    #     if p.pid == 0:
    #         p_menu = {
    #             "id": p.id,
    #             "pid": p.pid,
    #             "name": p.menu_name,
    #             "path": p.menu_path,
    #             "children": list()
    #         }
    #         for s in menu_list:
    #             if p.id == s.pid:
    #                 s_menu = {
    #                     "id": s.id,
    #                     "pid": s.pid,
    #                     "name": s.menu_name,
    #                     "path": s.menu_path,
    #                 }
    #                 p_menu.get("children").append(s_menu)
    #         p_menu['children'] = sorted(p_menu['children'], key=lambda x: x['id'])
    #         response_data.append(p_menu)
    response_json = {"data": response_data}
    return response_json


@roles_router.delete("/RoleMenu")
async def delete_role_menu(info: RoleAbout,
                           dbs: AsyncSession = Depends(db_session)):
    """
        删除菜单关联 根据role

    :param info:

        角色id，菜单id

    :param dbs:

        数据库依赖

    :return:


    """
    filter_condition = [
        ("role_id", f"=='{info.role_id}'", info.role_id),
        ("menu_id", f".in_({info.ids})", info.ids)
    ]
    await RoleMenuMapping.filter_delete_data(dbs, *filter_condition)
    response_json = {"data": info.ids}
    return response_json


@roles_router.post("/RoleMenu")
async def add_role_menu(info: RoleAbout, dbs: AsyncSession = Depends(db_session)):
    """增加菜单关联 根据role"""
    uid_list, exist_list = await RoleMenuMapping.filter_add_data_many(dbs, "role_id", info.role_id, "menu_id", info.ids)
    response_json = {"data": uid_list, "exist_data": exist_list}
    return response_json


@roles_router.get('/')
async def get_roles(info: SearchRole = Depends(SearchRole),
                    dbs: AsyncSession = Depends(db_session)):
    """
    获取角色列表
    :param info:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('role', f'.like(f"%{info.role}%")', info.role),
        ('creator', f'.like(f"%{info.creator}%")', info.creator),
        ('is_delete', '==0', 0)
    ]
    result, count, total_page = await Roles.get_all_detail_page(dbs, info.page, info.page_size, *filter_condition)
    new_result = []
    for res in result:
        new_res = {
            "create_time": res.create_time.strftime("%Y-%m-%d"),
            "creator": res.creator,
            "id": res.id,
            "is_delete": res.is_delete,
            "role": res.role,
            "update_time": res.update_time.strftime("%Y-%m-%d")
        }
        new_result.append(new_res)
    response_json = {"total": count,
                     "page": info.page,
                     "page_size": info.page_size,
                     "total_page": total_page,
                     "data": new_result}
    return response_json


@roles_router.get('/detail')
async def get_role_one(role_id: Optional[int] = Query(None), dbs: AsyncSession = Depends(db_session)):
    """
    获取某个角色的信息
    :param role_id:
    :param dbs:
    :return:
    """
    filter_condition = [
        ('role_id', f'=={role_id}', role_id),
        ('is_delete', '==0', 0)
    ]
    results = await RolePermissionMapping.get_all(dbs, *filter_condition)
    permission_id_list = [i.permission_id for i in results]
    role_menu_results = await RoleMenuMapping.get_all(dbs, *filter_condition)
    menu_id_list = [i.menu_id for i in role_menu_results]
    return {
        "data": await Roles.get_one_detail(dbs, role_id),
        "permission_id_list": permission_id_list,
        "menu_id_list": menu_id_list
    }


@roles_router.delete('/')
async def delete_roles(ids: Optional[List[int]] = Query(...), dbs: AsyncSession = Depends(db_session)):
    """
    删除角色 可批量
    :param ids:
    :param dbs:
    :return:
    """
    result = await Roles.delete_data(dbs, tuple(ids), auto_commit=False)

    if not result:
        raise HTTPException(status_code=404, detail="Delete non-existent resources.")
    filter_condition = [
        ("role_id", f".in_({ids})", ids)
    ]
    # 删除用户关联
    await RoleUserMapping.filter_delete_data(dbs, *filter_condition, auto_commit=False)
    # 删除部门关联
    await DepartmentRoleMapping.filter_delete_data(dbs, *filter_condition, auto_commit=False)
    # 删除菜单关联
    await RoleMenuMapping.filter_delete_data(dbs, *filter_condition, auto_commit=False)
    # 删除权限关联
    await RolePermissionMapping.filter_delete_data(dbs, *filter_condition, auto_commit=True)
    response_json = {"data": ids}
    return response_json


@roles_router.post('/')
async def create_role(role: AddRole, dbs: AsyncSession = Depends(db_session)):
    """
    创建角色
    :param role:
    :param dbs:
    :return:
    """
    role_add = {"role": role.role, "creator": role.creator}
    # 添加角色
    role_uid = await Roles.add_data(dbs, role_add)
    response_json = role.dict()
    # 添加默认拥有权限permission_id：查看用户详情61 ，角色菜单查看11，查看部门62，用户密码修改28，头像新增29, 角色查看15， 角色其他账户新增22
    permission_ids = [61, 11, 62, 28, 29, 15, 22]
    await RolePermissionMapping.filter_add_data_many(dbs, "role_id", role_uid,
                                                     "permission_id", permission_ids)
    response_json["id"] = role_uid
    return response_json


@roles_router.patch('/')
async def update_role(role: UpdateRole, dbs: AsyncSession = Depends(db_session)):
    """
    修改角色信息
    :param role:
    :param dbs:
    :return:
    """
    role_data_dict = role.dict(exclude_unset=True)
    result = await Roles.update_data(dbs, role_data_dict, is_delete=0)
    if not result:
        raise HTTPException(status_code=403, detail="User does not exist.")
    response_json = {"data": role_data_dict}
    return response_json


@roles_router.post('/RolePermission')
async def add_role_permission(info: RoleAbout, dbs: AsyncSession = Depends(db_session)):
    """增加权限关联 根据role"""
    uid_list, exist_list = await RolePermissionMapping.filter_add_data_many(dbs, "role_id", info.role_id,
                                                                            "permission_id", info.ids)
    response_json = {"data": uid_list, "exist_data": exist_list}
    return response_json


@roles_router.delete("/RolePermission")
async def delete_role_permission(info: RoleAbout,
                                 dbs: AsyncSession = Depends(db_session)):
    """删除权限关联 根据role"""
    filter_condition = [
        ("role_id", f"=='{info.role_id}'", info.role_id),
        ("permission_id", f".in_({info.ids})", info.ids)
    ]
    await RolePermissionMapping.filter_delete_data(dbs, *filter_condition)
    response_json = {"data": info.ids}
    return response_json


@roles_router.post("/RoleUser")
async def add_role_user(info: RoleAbout, dbs: AsyncSession = Depends(db_session)):
    """增加用户关联 根据role"""
    uid_list, exist_list = await RoleUserMapping.filter_add_data_many(dbs, "role_id", info.role_id, "user_id",
                                                                      info.ids)
    response_json = {"data": uid_list, "exist_data": exist_list}
    return response_json


@roles_router.delete("/RoleUser")
async def delete_role_user(info: RoleAbout,
                           dbs: AsyncSession = Depends(db_session)):
    """删除权限关联 根据role"""
    filter_condition = [
        ("role_id", f"=='{info.role_id}'", info.role_id),
        ("user_id", f".in_({info.ids})", info.ids)
    ]
    await RoleUserMapping.filter_delete_data(dbs, *filter_condition)
    response_json = {"data": info.ids}
    return response_json


@roles_router.post("/RoleAccount")
async def add_role_account(info: RoleAbout, dbs: AsyncSession = Depends(db_session)):
    """添加账号模块关联 根据role"""
    uid_list, exist_list = await RoleAccountMapping.filter_add_data_many(dbs, "role_id", info.role_id, "account_id",
                                                                         info.ids)
    response_json = {"data": uid_list, "exist_data": exist_list}
    return response_json


@roles_router.delete("/RoleAccount")
async def delete_role_account(info: RoleAbout, dbs: AsyncSession = Depends(db_session)):
    """删除账号模块关联 根据role"""
    filter_condition = [
        ("role_id", f"=='{info.role_id}'", info.role_id),
        ("account_id", f".in_({info.ids})", info.ids)
    ]
    await RoleAccountMapping.filter_delete_data(dbs, *filter_condition)
    response_json = {"data": info.ids}
    return response_json
