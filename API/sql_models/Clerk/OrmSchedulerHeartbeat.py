import datetime
from sql_models import create_table
from sql_models.db_config import BaseType, PBaseModel


class Heartbeat(PBaseModel):
    __tablename__ = 'heartbeat'

    job_name = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False, unique=True, comment='任务名')
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now,
                                      comment='创建时间')
    last_heartbeat = BaseType.BaseColumn(BaseType.BaseDateTime, comment='上次心跳时间')
    heartbeat_alarm = BaseType.BaseColumn(BaseType.BaseDateTime, comment='心跳断开时报警时间')
    interval = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False, comment='心跳间隔')
    alarm = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False, comment='是否启用:0-否；1-是')
    state = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False, default=2, comment='状态:0-正常；1-异常；2-离线')
    at = BaseType.BaseColumn(BaseType.BaseString(510), comment='@的用户:all-所有人；手机号,手机号-被@人的手机号，英文逗号分割')
    type = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False, default="serve",
                               comment='类型:machine-机器；serve-服务')


# 当Heartbeat表type字段为machine时，使用此表查询机器对应ip
class Machine(PBaseModel):
    __tablename__ = 'machine'

    machine_ip = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False, unique=True, comment='机器ip')
    scope = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False, unique=True, comment='范围,例：1-60')
    restart_authorization = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False, default=1,
                                                comment='重启授权:0-关闭；1-开启')


if __name__ == '__main__':
    create_table()
