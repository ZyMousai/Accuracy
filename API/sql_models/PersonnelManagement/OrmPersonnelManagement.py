import datetime

from sql_models import create_table
from sql_models.db_config import BaseType, PBaseModel

from sqlalchemy import select


class Users(PBaseModel):
    __tablename__ = 'users'
    account = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False, unique=True)  # 用户名
    password = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # 密码
    name = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 姓名
    gender = BaseType.BaseColumn(BaseType.BaseBoolean, nullable=False)  # 性别
    birth = BaseType.BaseColumn(BaseType.BaseDate, nullable=False)  # 出生日期
    entry_time = BaseType.BaseColumn(BaseType.BaseDate, nullable=False)  # 入职时间
    phone = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 电话
    address = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 地址
    avatar = BaseType.BaseColumn(BaseType.BaseString(88), nullable=True, default='0')  # 头像的路径
    creator = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False, default='admin')  # 创建人
    update_password_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False,
                                               default=datetime.datetime.now() - datetime.timedelta(days=30))  # 密码修改时间

    @classmethod
    async def add_data(cls, dbs, info, auto_commit=True):
        _orm = select(cls).where(cls.is_delete == 0, cls.account == info.account)
        result = (await dbs.execute(_orm)).scalars().first()
        uid = 0
        if not result:
            user = cls(**info.dict())
            dbs.add(user)
            await dbs.flush()
            uid = user.id
            if auto_commit:
                await dbs.commit()
        return uid

    @classmethod
    async def get_user_department(cls, dbs, department_id):
        _orm = select(cls).outerjoin(DepartmentUserMapping, cls.id == DepartmentUserMapping.user_id). \
            where(cls.is_delete == 0, DepartmentUserMapping.department_id == department_id)
        result = (await dbs.execute(_orm)).scalars().all()
        return result


class Roles(PBaseModel):
    __tablename__ = 'roles'
    role = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 角色
    creator = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 创建人
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now())  # 创建时间
    update_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now)  # 更新时间

    @classmethod
    async def get_role_user(cls, dbs, user_id):
        """
        返回的字段仅含有主表的
        :param dbs: 依赖数据库
        :param user_id: 对应的user的id
        :return:
        """
        _orm = select(cls).outerjoin(RoleUserMapping,
                                     cls.id == RoleUserMapping.role_id).where(cls.is_delete == 0,
                                                                              RoleUserMapping.user_id == user_id)
        result = (await dbs.execute(_orm)).scalars().first()
        return result

    @classmethod
    async def get_role_department(cls, dbs, department_id):
        _orm = select(cls).outerjoin(DepartmentRoleMapping, cls.id == DepartmentRoleMapping.role_id). \
            where(cls.is_delete == 0, DepartmentRoleMapping.department_id == department_id)
        result = (await dbs.execute(_orm)).scalars().all()
        return result


class RoleUserMapping(PBaseModel):
    __tablename__ = 'role_user_mapping'
    role_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 角色id
    user_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 用户id


class Permission(PBaseModel):
    __tablename__ = 'permission'
    p_url = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # 权限url
    p_method = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # 方法
    operate = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 操作 1.新增 2.修改 3.查看 4.删除

    @classmethod
    async def filter_get_permission(cls, dbs, role_id, url, method):
        filter_c = [
            cls.is_delete == 0, RolePermissionMapping.role_id == role_id,
            cls.p_url == url, cls.p_method == method
        ]
        _orm = select(cls).outerjoin(RolePermissionMapping, cls.id == RolePermissionMapping.permission_id).where(
            *filter_c)
        result = (await dbs.execute(_orm)).first()
        return result


class RolePermissionMapping(PBaseModel):
    __tablename__ = 'role_permission_mapping'
    role_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 角色id
    permission_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 权限id


class RoleAccountMapping(PBaseModel):
    __tablename__ = 'role_account_mapping'
    role_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 角色id
    account_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 账户id


class Menu(PBaseModel):
    __tablename__ = 'menu'
    pid = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False, default=0)  # 父级id
    menu_name = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 菜单名
    menu_path = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # 菜单路径

    @classmethod
    async def get_menu_role(cls, dbs, role_id):
        _orm = select(cls).outerjoin(RoleMenuMapping,
                                     cls.id == RoleMenuMapping.menu_id).where(cls.is_delete == 0,
                                                                              RoleMenuMapping.role_id == role_id)
        result = (await dbs.execute(_orm)).scalars().all()
        return result


class RoleMenuMapping(PBaseModel):
    __tablename__ = 'role_menu_mapping'
    menu_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 菜单id
    role_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 角色id


class Departments(PBaseModel):
    __tablename__ = 'department'
    department = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 部门名
    creator = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 创建人
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now())  # 创建时间

    @classmethod
    async def get_department_role(cls, dbs, role_id):
        _orm = select(cls).outerjoin(DepartmentRoleMapping,
                                     cls.id == DepartmentRoleMapping.department_id).where(cls.is_delete == 0,
                                                                                          DepartmentRoleMapping.role_id == role_id)
        result = (await dbs.execute(_orm)).scalars().first()
        return result


class DepartmentUserMapping(PBaseModel):
    __tablename__ = 'department_user_mapping'
    department_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 部门id
    user_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 用户id

    @classmethod
    async def filter_add_data_many_(cls, dbs, department_id, ids, auto_commit=True):
        # 先查询出有没有相关数据
        add_list = [{"department_id": department_id, "user_id": x} for x in ids]
        add_user_id_list = []
        exist_list = []
        _orm = select(cls).where(cls.is_delete == 0, cls.department_id == department_id, cls.user_id.in_(ids))
        exist_data = (await dbs.execute(_orm)).scalars().all()
        exist_data_id = [o.user_id for o in exist_data]
        # 只会插入不存在的数据
        for info in add_list:
            if info.get('user_id') not in exist_data_id:
                await cls.add_data(dbs, info, auto_commit=False)
                add_user_id_list.append(info.get('user_id'))
            else:
                exist_list.append(info.get('user_id'))
        if auto_commit:
            await dbs.commit()
        return add_user_id_list, exist_data_id


class DepartmentRoleMapping(PBaseModel):
    __tablename__ = 'department_role_mapping'
    department_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 部门id
    role_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 角色id

    @classmethod
    async def filter_add_data_many_(cls, dbs, department_id, ids, auto_commit=True):
        # 先查询出有没有相关数据
        add_list = [{"department_id": department_id, "role_id": x} for x in ids]
        add_role_id_list = []
        exist_list = []
        _orm = select(cls).where(cls.is_delete == 0, cls.department_id == department_id, cls.role_id.in_(ids))
        exist_data = (await dbs.execute(_orm)).scalars().all()
        exist_data_id = [o.role_id for o in exist_data]
        # 只会插入不存在的数据
        for info in add_list:
            if info.get('role_id') not in exist_data_id:
                await cls.add_data(dbs, info, auto_commit=False)
                add_role_id_list.append(info.get('role_id'))
            else:
                exist_list.append(info.get('role_id'))
        if auto_commit:
            await dbs.commit()
        return add_role_id_list, exist_data_id


if __name__ == '__main__':
    create_table()
