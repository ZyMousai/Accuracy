# Roles 视图
from typing import Optional, List

from fastapi import APIRouter, Depends, Request, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sql_models.PersonnelManagement.OrmPersonnelManagement import Roles, Menu, RoleMenuMapping
from sql_models.db_config import db_session

roles_router = APIRouter(
    prefix="/roles/v1",
    responses={404: {"description": "Not found"}}, )


def get_role_id(request: Request):
    # return request.state.role_id
    return 1


@roles_router.get("/RoleMenu")
async def get_role_menu(dbs: AsyncSession = Depends(db_session), role_id=Depends(get_role_id)):
    """获取菜单 根据role"""

    # 根据role获取菜单
    menu_list = await Menu.get_menu_role(dbs, role_id)
    response_data = []
    for p in menu_list:
        if p.pid == 0:
            p_menu = {
                "id": p.id,
                "pid": p.pid,
                "menu_name": p.menu_name,
                "menu_path": p.menu_path,
                "son_menu": list()
            }
            for s in menu_list:
                if p.id == s.pid:
                    s_menu = {
                        "id": s.id,
                        "pid": s.pid,
                        "menu_name": s.menu_name,
                        "menu_path": s.menu_path,
                    }
                    p_menu['son_menu'].append(s_menu)
            p_menu['son_menu'] = sorted(p_menu['son_menu'], key=lambda x: x['id'])
            response_data.append(p_menu)

    response_json = {"data": response_data}
    return response_json


@roles_router.delete("/RoleMenu")
async def delete_role_menu(ids: Optional[List[int]] = Query(...), dbs: AsyncSession = Depends(db_session),
                           role_id=Depends(get_role_id)):
    """删除菜单关联 根据role"""
    filter_condition = [
        ("role_id", f"=='{role_id}'", role_id),
        ("menu_id", f".in_({ids})", ids)
    ]
    await RoleMenuMapping.filter_delete_data(dbs, *filter_condition)
    response_json = {"data": ids}
    return response_json


@roles_router.post("/RoleMenu")
async def add_role_menu(ids: Optional[List[int]] = Query(...), dbs: AsyncSession = Depends(db_session),
                        role_id=Depends(get_role_id)):
    """增加菜单关联 根据role"""
    uid_list, exist_list = await RoleMenuMapping.add_data_many_(dbs, role_id, ids)
    response_json = {"data": uid_list, "exist_data": exist_list}
    return response_json
