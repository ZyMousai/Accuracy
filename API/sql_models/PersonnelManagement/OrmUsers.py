import datetime
from sql_models import create_table
from sql_models.db_config import Base, BaseType


class User(Base):
    __tablename__ = 'user'
    id = BaseType.BaseColumn(BaseType.BaseInteger, primary_key=True)
    account = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False, unique=True)  # 用户名
    password = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # 密码
    name = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 姓名
    gender = BaseType.BaseColumn(BaseType.BaseBoolean, nullable=False)  # 性别
    birth = BaseType.BaseColumn(BaseType.BaseDate, nullable=False)  # 出生日期
    entry_time = BaseType.BaseColumn(BaseType.BaseDate, nullable=False)  # 入职时间
    phone = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 电话
    address = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 地址
    roles = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 关联的角色
    department = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 部门
    avatar = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # 头像
    is_delete = BaseType.BaseColumn(BaseType.BaseBoolean, nullable=False, default=False)  # 逻辑删除

    @classmethod
    async def get_one(cls, dbs, user_id):
        return await dbs.get(cls, user_id)


class Role(Base):
    __tablename__ = 'role'
    id = BaseType.BaseColumn(BaseType.BaseInteger, primary_key=True)
    role = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 角色
    creator = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)  # 创建人
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now())  # 创建时间
    update_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now)  # 创建时间


if __name__ == '__main__':
    create_table()
