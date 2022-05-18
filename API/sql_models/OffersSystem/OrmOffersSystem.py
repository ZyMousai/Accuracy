import datetime

from sql_models import create_table
from sql_models.db_config import BaseType, PBaseModel


# outerjoin查询仅返回主表内容

class OffersUnion(PBaseModel):
    __tablename__ = 'offers_union'
    union_name = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False, unique=True)  # 联盟名字
    union_url = BaseType.BaseColumn(BaseType.BaseString(188), nullable=False)  # 联盟地址
    union_system_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 追踪系统 id
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now())  # 创建时间


class UnionSystem(PBaseModel):
    __tablename__ = 'union_system'
    union_system = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False, unique=True)  # 联盟系统


class OffersAccount(PBaseModel):
    __tablename__ = 'offers_account'
    union_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 联盟id
    offers_account = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # 账户
    offers_pwd = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # 密码
    offers_api_key = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # api key
    options = BaseType.BaseColumn(BaseType.BaseJson)  # api key
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now())  # 创建时间


class Offers(PBaseModel):
    __tablename__ = 'offers'
    union_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 联盟id
    account_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 账号id
    offers_name = BaseType.BaseColumn(BaseType.BaseString(288), nullable=False)  # 任务名
    offers_desc = BaseType.BaseColumn(BaseType.BaseText)  # 任务描述
    pay = BaseType.BaseColumn(BaseType.BaseInteger)  # 佣金
    pay_unit = BaseType.BaseColumn(BaseType.BaseString(288))  # 佣金单位
    offers_url = BaseType.BaseColumn(BaseType.BaseString(288))  # 任务链接
    remark = BaseType.BaseColumn(BaseType.BaseText)  # 备注


if __name__ == '__main__':
    create_table()
