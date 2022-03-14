# 权限验证
from sql_models.PersonnelManagement.OrmPersonnelManagement import RoleAccountMapping, Permission, RoleUserMapping
from sql_models.db_config import db_session2
from fastapi import Request


class AuthPermissions(object):
    @staticmethod
    async def auth(request: Request):
        # 认证标志
        auth_tag = False

        # 获取参数
        url = str(request.url.path)
        method = request.method
        role_id = request.state.role_id
        user_id = request.state.user_id

        # 连接数据库
        dbs = await db_session2()

        # 验证用户和角色是否存在关联
        filter_c = [
            ("user_id", f"=={user_id}", user_id),
            ("role_id", f"=={role_id}", role_id)
        ]
        r = await RoleUserMapping.get_one(dbs, *filter_c)

        if not r:
            return auth_tag

        # 验证权限是否存在
        r = await Permission.filter_get_permission(dbs, role_id, url, method)
        if r:
            auth_tag = True

        await dbs.close()
        return auth_tag
