# coding: utf-8
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sql_models.db_config import BaseType, PBaseModel
import datetime


class TbAccount(PBaseModel):
    __tablename__ = 'tb_Account'

    id = BaseType.BaseColumn(BaseType.BaseInteger, primary_key=True)
    account_name = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False)  # 账号名


class TbAlliance(PBaseModel):
    __tablename__ = 'tb_Alliance'

    id = BaseType.BaseColumn(BaseType.BaseInteger, primary_key=True)
    alliance_name = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False)  # 联盟名称


class TbCard(PBaseModel):
    __tablename__ = 'tb_Card'

    id = BaseType.BaseColumn(BaseType.BaseInteger, primary_key=True)
    card_number = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False, unique=True)  # 卡号
    face_value = BaseType.BaseColumn(BaseType.BaseFloat(asdecimal=True), nullable=False)  # 面值
    valid_period = BaseType.BaseColumn(BaseType.BaseString(255))  # 有效期
    cvv = BaseType.BaseColumn(BaseType.BaseString(255))  # cvv
    card_status = BaseType.BaseColumn(BaseType.BaseBoolean(1))  # 卡状态
    name = BaseType.BaseColumn(BaseType.BaseString(255))  # 卡姓名地址
    platform = BaseType.BaseColumn(BaseType.BaseString(255))  # 开卡平台
    note = BaseType.BaseColumn(BaseType.BaseString(255))  # 备注
    card_name = BaseType.BaseColumn(BaseType.BaseString(255))  # 卡名称
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now())  # 创建时间
    retain = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 是否保留 0-否,1-是
    is_delete = BaseType.BaseColumn(BaseType.BaseBoolean(1))  # 逻辑删除


class TbTask(PBaseModel):
    __tablename__ = 'tb_Task'

    id = BaseType.BaseColumn(BaseType.BaseInteger, primary_key=True)
    card_id = BaseType.BaseColumn(ForeignKey('tb_Card.id'), nullable=False, index=True)  # 卡id
    creation_date = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now())  # 创建日期
    account_id = BaseType.BaseColumn(ForeignKey('tb_Account.id'), nullable=False, index=True)  # 联盟id
    alliance_id = BaseType.BaseColumn(ForeignKey('tb_Alliance.id'), nullable=False, index=True)  # 账号id
    task = BaseType.BaseColumn(BaseType.BaseString(255))  # 任务
    commission = BaseType.BaseColumn(BaseType.BaseFloat(asdecimal=True))  # 佣金
    consume = BaseType.BaseColumn(BaseType.BaseFloat(asdecimal=True), nullable=False)  # 消耗
    user = BaseType.BaseColumn(BaseType.BaseString(255))  # 使用人
    secondary_consumption = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 是否二次消费 0-否,1-是
    is_delete = BaseType.BaseColumn(BaseType.BaseBoolean(1))  # 逻辑删除

    account = relationship('TbAccount')
    alliance = relationship('TbAlliance')
    card = relationship('TbCard')
