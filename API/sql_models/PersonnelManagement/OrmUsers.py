import datetime
from sql_models import create_table
from sql_models.db_config import BaseType, PBaseModel


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
    avatar = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # 头像的路径


class Roles(PBaseModel):
    __tablename__ = 'roles'
    role = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 角色
    creator = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 创建人
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now())  # 创建时间
    update_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now)  # 更新时间


class RoleUserMapping(PBaseModel):
    __tablename__ = 'role_user_mapping'
    role_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 角色id
    user_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 用户id


class Permission(PBaseModel):
    __tablename__ = 'permission'
    menu_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 菜单id
    operate = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 操作 1.新增 2.修改 3.查看 4.删除 5.搜索 6.菜单显示


class Menu(PBaseModel):
    __tablename__ = 'menu'
    pid = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False, default=0)  # 父级id
    menu_name = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 菜单名
    menu_path = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # 菜单路径


class RolePermissionMapping(PBaseModel):
    __tablename__ = 'role_permission_mapping'
    role_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 角色id
    permission_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 权限id


class Departments(PBaseModel):
    __tablename__ = 'department'
    department = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 部门名
    creator = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 创建人
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now())  # 创建时间


class DepartmentUserMapping(PBaseModel):
    __tablename__ = 'department_user_mapping'
    department_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 部门id
    user_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 用户id


class DepartmentRoleMapping(PBaseModel):
    __tablename__ = 'department_role_mapping'
    department_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 部门id
    role_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 角色id


if __name__ == '__main__':
    create_table()
