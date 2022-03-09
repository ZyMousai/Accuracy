import datetime

from sql_models import create_table
from sql_models.db_config import BaseType, PBaseModel
from sqlalchemy import select, func, delete
from sqlalchemy import select


class Server(PBaseModel):
    __tablename__ = 'servers'

    name = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False, unique=True)
    ip_address = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)
    password = BaseType.BaseColumn(BaseType.BaseString(50), nullable=True)
    pass_key = BaseType.BaseColumn(BaseType.BaseString(50), nullable=True)  # 存储密钥保存路径
    remark = BaseType.BaseColumn(BaseType.BaseString(255), nullable=True)


class ServerScript(PBaseModel):
    __tablename__ = 'server_script'
    server_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)
    task_name = BaseType.BaseColumn(BaseType.BaseString(100), nullable=False)
    order = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False)  # 执行代码
    process_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)
    timing = BaseType.BaseColumn(BaseType.BaseString(100), nullable=False)
    last_execute_user = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)
    last_execution_time = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)
    next_execution_time = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)
    create_user = BaseType.BaseColumn(BaseType.BaseString(30), nullable=False)
    status = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 0 失败  1 成功  2运行中

    @classmethod
    async def delete_data_server_id(cls, dbs, server_ids):
        '''
        根据服务器id删除对应的脚本数据
        :param dbs:
        :param server_ids:
        :return:
        '''
        _orm = delete(cls).where(cls.server_id.in_(server_ids))
        (await dbs.execute(_orm))

        await dbs.flush()
        await dbs.commit()

        return server_ids
