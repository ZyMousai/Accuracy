import datetime

from sql_models import create_table
from sql_models.db_config import BaseType, PBaseModel
from starlette.responses import JSONResponse
from sqlalchemy import select, func, delete


# outerjoin查询仅返回主表内容

class OffersUnion(PBaseModel):
    __tablename__ = 'offers_union'
    union_name = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False, unique=True)  # 联盟名字
    union_url = BaseType.BaseColumn(BaseType.BaseString(188), nullable=False)  # 联盟地址
    union_system_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 追踪系统 id
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now())  # 创建时间

    @classmethod
    async def get_all_detail_page_associated(cls, dbs, page, page_size, *args):
        """获取所有数据-分页"""
        try:
            # 构建查询条件
            filter_condition = list()
            for x in args:
                if x[2] is not None:
                    filter_condition.append(eval(f'cls.{x[0]}{x[1]}'))
            # 处理分页
            count = await cls.get_data_count(dbs, *filter_condition)
            remainder = count % page_size
            if remainder == 0:
                total_page = int(count // page_size)
            else:
                total_page = int(count // page_size) + 1

            # 查询数据
            # scalars主要作用是把数据映射到orm类上去，不然得到的就是一行一行的查询结果

            _orm = select(cls.id, cls.union_name, cls.union_url, UnionSystem.union_system, cls.union_system_id,
                          func.date_format(cls.create_time, "%Y-%m-%d %H:%i:%S")).outerjoin(UnionSystem,
                                                                                            UnionSystem.id == cls.union_system_id).where(
                *filter_condition).order_by().limit(
                page_size).offset((page - 1) * page_size)

            result = (await dbs.execute(_orm)).all()

        except Exception as e:
            return JSONResponse(status_code=400, content={"detail": str(e)})
        return result, count, total_page


class UnionSystem(PBaseModel):
    __tablename__ = 'union_system'
    union_system = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False, unique=True)  # 联盟系统
    union_system_api_url = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False, unique=True)  # 联盟系统api_url


class OffersAccount(PBaseModel):
    __tablename__ = 'offers_account'
    union_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 联盟id
    offers_account = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # 账户
    offers_pwd = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # 密码
    offers_api_key = BaseType.BaseColumn(BaseType.BaseString(88), nullable=False)  # api key
    options = BaseType.BaseColumn(BaseType.BaseJson)  # api key
    status = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)
    ip_info = BaseType.BaseColumn(BaseType.BaseJson)
    create_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now())  # 创建时间

    @classmethod
    async def get_all_detail_page_associated(cls, dbs, page, page_size, *args):
        """获取所有数据-分页"""
        try:
            # 构建查询条件
            filter_condition = list()
            for x in args:
                if x[2] is not None:
                    filter_condition.append(eval(f'{x[0]}{x[1]}'))
            # 处理分页
            _orm_count = select(func.count(cls.id)).outerjoin(OffersUnion,
                                                              cls.union_id == OffersUnion.id).where(*filter_condition)

            count = (await dbs.execute(_orm_count)).scalar()
            remainder = count % page_size
            if remainder == 0:
                total_page = int(count // page_size)
            else:
                total_page = int(count // page_size) + 1

            # 查询数据
            # scalars主要作用是把数据映射到orm类上去，不然得到的就是一行一行的查询结果

            _orm = select(cls.id, OffersUnion.union_name, cls.offers_account, cls.offers_pwd, cls.offers_api_key,
                          cls.status, cls.ip_info, cls.options, cls.union_id).outerjoin(OffersUnion,
                                                                                        OffersUnion.id == cls.union_id).where(
                *filter_condition).order_by().limit(
                page_size).offset((page - 1) * page_size)


            result = (await dbs.execute(_orm)).all()

        except Exception as e:
            return JSONResponse(status_code=400, content={"detail": str(e)})
        return result, count, total_page


class Offers(PBaseModel):
    __tablename__ = 'offers'
    union_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 联盟id
    account_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)  # 账号id
    offers_name = BaseType.BaseColumn(BaseType.BaseString(288), nullable=False)  # 任务名
    offers_desc = BaseType.BaseColumn(BaseType.BaseText)  # 任务描述
    country = BaseType.BaseColumn(BaseType.BaseString(28))  # 国家
    pay = BaseType.BaseColumn(BaseType.BaseInteger)  # 佣金
    pay_unit = BaseType.BaseColumn(BaseType.BaseString(288))  # 佣金单位
    offers_url = BaseType.BaseColumn(BaseType.BaseString(288))  # 任务链接
    remark = BaseType.BaseColumn(BaseType.BaseText)  # 备注

    @classmethod
    async def get_all_detail_page_associated(cls, dbs, page, page_size, *args):
        """获取所有数据-分页"""
        # try:
        # 构建查询条件
        filter_condition = list()
        for x in args:
            if x[2] is not None:
                filter_condition.append(eval(f'cls.{x[0]}{x[1]}'))
        # 处理分页
        _orm_count = select(func.count(cls.id)).outerjoin(OffersUnion, cls.union_id == OffersUnion.id).outerjoin(
            OffersAccount, cls.account_id == OffersAccount.id).where(*filter_condition)

        count = (await dbs.execute(_orm_count)).scalar()
        remainder = count % page_size
        if remainder == 0:
            total_page = int(count // page_size)
        else:
            total_page = int(count // page_size) + 1

        # 查询数据
        # scalars主要作用是把数据映射到orm类上去，不然得到的就是一行一行的查询结果

        _orm = select(cls.id, cls.union_id, OffersUnion.union_name,
                      cls.account_id, OffersAccount.offers_account,
                      cls.offers_name, cls.offers_desc, cls.country,
                      cls.pay, cls.pay_unit, cls.offers_url, cls.remark)\
            .outerjoin(OffersUnion, cls.union_id == OffersUnion.id)\
            .outerjoin(OffersAccount, cls.account_id == OffersAccount.id)\
            .where(*filter_condition).order_by().limit(page_size).offset((page - 1) * page_size)

        result = (await dbs.execute(_orm)).all()

        # except Exception as e:
        #     return JSONResponse(status_code=400, content={"detail": str(e)})
        return result, count, total_page


if __name__ == '__main__':
    create_table()
