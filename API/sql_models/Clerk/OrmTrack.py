import datetime

from sqlalchemy import select

from sql_models import create_table
from sql_models.db_config import BaseType, PBaseModel


class TrackAlliance(PBaseModel):
    __tablename__ = 'track_alliance'

    name = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False)
    url = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False)
    created_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now)

    @classmethod
    async def get_all_detail_page(cls, dbs, page, page_size, *args):
        """获取所有数据-分页-关联查询"""
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
        _orm = select(cls.id, cls.name, cls.url, TrackUrl.track_url).outerjoin(TrackUrl,
                                                                               TrackUrl.alliance_id == cls.id).where(
            *filter_condition).order_by().limit(page_size).offset((page - 1) * page_size)
        result = (await dbs.execute(_orm)).all()

        return result, count, total_page


class TrackUrl(PBaseModel):
    __tablename__ = 'track_url'

    track_url = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False)
    alliance_id = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)
    created_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now)


if __name__ == '__main__':
    create_table()
