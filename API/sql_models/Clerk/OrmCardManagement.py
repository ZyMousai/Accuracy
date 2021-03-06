# coding: utf-8
import datetime

from sqlalchemy import select
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sql_models.db_config import BaseType, PBaseModel
from sql_models import create_table


class TbAccount(PBaseModel):
    __tablename__ = 'tb_Account'

    # account_name = BaseType.BaseColumn(BaseType.BaseString(255))  # 账号名
    uid = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False)  # uid


# class TbAlliance(PBaseModel):
#     __tablename__ = 'tb_Alliance'
#
#     alliance_name = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False)  # 联盟名称


class TbCard(PBaseModel):
    __tablename__ = 'tb_Card'

    card_number = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False, unique=True)  # 卡号
    face_value = BaseType.BaseColumn(BaseType.BaseFloat(asdecimal=True), nullable=False)  # 面值
    valid_period = BaseType.BaseColumn(BaseType.BaseString(255))  # 有效期
    cvv = BaseType.BaseColumn(BaseType.BaseString(255))  # cvv
    card_status = BaseType.BaseColumn(BaseType.BaseInteger)  # 卡状态 0-不可用,1-可用
    name = BaseType.BaseColumn(BaseType.BaseString(255))  # 卡姓名地址
    platform = BaseType.BaseColumn(BaseType.BaseString(255))  # 开卡平台
    note = BaseType.BaseColumn(BaseType.BaseString(255))  # 备注
    card_name = BaseType.BaseColumn(BaseType.BaseString(255))  # 卡名称
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now)  # 创建时间
    retain = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False, default=False)  # 是否保留 0-否,1-是

    @classmethod
    async def get_card_task(cls, dbs, card_id):
        _orm = select(cls).outerjoin(TbTask, cls.id == TbTask.card_id). \
            where(cls.is_delete == 0, TbTask.card_id == card_id)
        result = (await dbs.execute(_orm)).scalars().all()
        return result


class TbTask(PBaseModel):
    __tablename__ = 'tb_Task'

    card_id = BaseType.BaseColumn(ForeignKey('tb_Card.id'), nullable=False, index=True)  # 卡id
    account_id = BaseType.BaseColumn(ForeignKey('tb_Account.id'), nullable=False, index=True)  # uid => id
    # alliance_id = BaseType.BaseColumn(ForeignKey('tb_Alliance.id'), nullable=False, index=True)  # 账号id
    creation_date = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now)  # 创建日期
    task = BaseType.BaseColumn(BaseType.BaseString(255))  # 任务
    commission = BaseType.BaseColumn(BaseType.BaseFloat(asdecimal=True))  # 佣金
    consume = BaseType.BaseColumn(BaseType.BaseFloat(asdecimal=True), nullable=False)  # 消耗
    user = BaseType.BaseColumn(BaseType.BaseString(255))  # 使用人
    secondary_consumption = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 是否二次消费 0-否,1-是
    note = BaseType.BaseColumn(BaseType.BaseString(255))  # 备注

    card = relationship('TbCard')
    account = relationship('TbAccount')

    # alliance = relationship('TbAlliance')

    @classmethod
    async def get_account_task(cls, dbs, uid):
        _orm = select(cls).outerjoin(TbAccount, cls.uid == uid). \
            where(cls.is_delete == 0)
        result = (await dbs.execute(_orm)).scalars().all()
        return result

    @classmethod
    async def get_task_account_consume_commission(cls, dbs, account_id, args):
        """
        获取对应account_id的任务的消耗和收益
        :param dbs: 数据库依赖
        :param account_id:  对应的account_id
        :return:
        """
        filter_condition = list()
        for x in args:
            if x[2] is not None:
                filter_condition.append(eval(f'cls.{x[0]}{x[1]}'))
        _orm = select(cls.consume, cls.commission).where(cls.is_delete == 0, cls.account_id == account_id, *filter_condition)
        # 注意这里没有加scalars()，才能得到所有的查询数据
        result = (await dbs.execute(_orm)).all()
        return result


if __name__ == '__main__':
    create_table()
