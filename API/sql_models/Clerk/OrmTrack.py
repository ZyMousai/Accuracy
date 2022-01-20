import datetime
from sql_models import create_table
from sql_models.db_config import BaseType, PBaseModel


class Alliance(PBaseModel):
    __tablename__ = 'track_alliance'

    name = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False)
    url = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False)
    created_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now)


class TraceUrl(PBaseModel):
    __tablename__ = 'trace_url'

    url = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False)
    allianceId = BaseType.BaseColumn(BaseType.BaseInteger, nullable=False)
    created_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False)


if __name__ == '__main__':
    create_table()
