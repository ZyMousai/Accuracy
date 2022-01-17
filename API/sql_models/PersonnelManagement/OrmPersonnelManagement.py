import datetime

from sqlalchemy.orm import selectinload

from sql_models import create_table
from sql_models.db_config import BaseType, PBaseModel

from sqlalchemy import select, join


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
    async def add_data(cls, dbs, info):
        _orm = select(cls).where(cls.is_delete == 0, cls.account == info.account)
        result = (await dbs.execute(_orm)).scalars().first()
        uid = 0
        if not result:
            user = cls(**info.dict())
            dbs.add(user)
            await dbs.flush()
            uid = user.id
            await dbs.commit()
        return uid


class Roles(PBaseModel):
    __tablename__ = 'roles'
    role = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 角色
    creator = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 创建人
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now())  # 创建时间
    update_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now)  # 更新时间

    @classmethod
    async def get_role_user(cls, dbs, user_id):
        _orm = select(cls).outerjoin(RoleUserMapping,
                                     cls.id == RoleUserMapping.role_id).where(cls.is_delete == 0,
                                                                              RoleUserMapping.user_id == user_id)
        result = (await dbs.execute(_orm)).scalars().first()
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


class RolePermissionMapping(PBaseModel):
    __tablename__ = 'role_permission_mapping'
    role_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 角色id
    permission_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 权限id


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

    @classmethod
    async def add_data_many_(cls, dbs, role_id, ids):
        # 先查询出有没有相关数据
        add_list = [{"role_id": role_id, "menu_id": x} for x in ids]
        add_menu_id_list = []
        exist_list = []
        _orm = select(cls).where(cls.is_delete == 0, cls.role_id == role_id, cls.menu_id.in_(ids))
        exist_data = (await dbs.execute(_orm)).scalars().all()
        exist_data_id = [o.menu_id for o in exist_data]
        # 只会插入不存在的数据
        for info in add_list:
            if info.get('menu_id') not in exist_data_id:
                await cls.add_data(dbs, info, auto_commit=False)
                add_menu_id_list.append(info.get('menu_id'))
            else:
                exist_list.append(info.get('menu_id'))
        await dbs.commit()
        return add_menu_id_list, exist_data_id


class Departments(PBaseModel):
    __tablename__ = 'department'
    department = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 部门名
    creator = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 创建人
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now())  # 创建时间


class DepartmentUserMapping(PBaseModel):
    __tablename__ = 'department_user_mapping'
    department_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 部门id
    user_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 用户id

    @classmethod
    async def add_data_many_(cls, dbs, user_id, ids):
        # 先查询出有没有相关数据
        add_list = [{"user_id": user_id, "department_id": x} for x in ids]
        add_department_list = []
        exist_list = []
        _orm = select(cls).where(cls.is_delete == 0, cls.user_id == user_id, cls.department_id.in_(ids))
        exist_data = (await dbs.execute(_orm)).scalars().all()
        exist_data_id = [o.department_id for o in exist_data]
        # 只会插入不存在的数据
        for info in add_list:
            if info.get('department_id') not in exist_data_id:
                await cls.add_data(dbs, info, auto_commit=False)
                add_department_list.append(info.get('department_id'))
            else:
                exist_list.append(info.get('department_id'))
        await dbs.commit()
        return add_department_list, exist_data_id


class DepartmentRoleMapping(PBaseModel):
    __tablename__ = 'department_role_mapping'
    department_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 部门id
    role_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 角色id

    @classmethod
    async def add_data_many_(cls, dbs, role_id, ids):
        # 先查询出有没有相关数据
        add_list = [{"role_id": role_id, "department_id": x} for x in ids]
        add_department_list = []
        exist_list = []
        _orm = select(cls).where(cls.is_delete == 0, cls.role_id == role_id, cls.department_id.in_(ids))
        exist_data = (await dbs.execute(_orm)).scalars().all()
        exist_data_id = [o.department_id for o in exist_data]
        # 只会插入不存在的数据
        for info in add_list:
            if info.get('department_id') not in exist_data_id:
                await cls.add_data(dbs, info, auto_commit=False)
                add_department_list.append(info.get('department_id'))
            else:
                exist_list.append(info.get('department_id'))
        await dbs.commit()
        return add_department_list, exist_data_id


if __name__ == '__main__':
    create_table()
