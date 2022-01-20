from sql_models import create_table
from sql_models.db_config import PBaseModel, BaseType


class Alliance(PBaseModel):
    __tablename__ = 'alliance'

    name = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False, unique=True)
    url = BaseType.BaseColumn(BaseType.BaseString(10), nullable=False)
    created_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False)
    status = BaseType.BaseColumn(BaseType.BaseBoolean, nullable=False, default=False)


class Traceurl(PBaseModel):
    __tablename__ = 'traceurl'

    url = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False, unique=True)
    allianceId = BaseType.BaseColumn(BaseType.BaseString(255), nullable=False)
    created_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False)



if __name__ == '__main__':
    create_table()