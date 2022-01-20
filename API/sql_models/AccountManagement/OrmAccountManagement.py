from sql_models import create_table
from sql_models.db_config import BaseType, PBaseModel


# 数据库
class Account(PBaseModel):
    __tablename__ = 'account'
    platform = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)
    account = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)
    password = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)
    remark = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False)


if __name__ == '__main__':
    create_table()
