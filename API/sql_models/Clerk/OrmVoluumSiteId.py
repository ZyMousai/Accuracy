from sql_models import create_table
from sql_models.db_config import BaseType, PBaseModel


# 数据库
class DBCampaignMapping(PBaseModel):
    # 对应的数据库的表的名称
    __tablename__ = 'campaign_mapping'

    m_id = BaseType.BaseColumn(BaseType.BaseString(188))
    m_name = BaseType.BaseColumn(BaseType.BaseString(588))
    s_id = BaseType.BaseColumn(BaseType.BaseString(188))
    s_name = BaseType.BaseColumn(BaseType.BaseString(588))


if __name__ == '__main__':
    create_table()
