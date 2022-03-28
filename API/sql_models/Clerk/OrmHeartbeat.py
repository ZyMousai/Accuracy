# import datetime
# import uuid
#
# from sqlalchemy import select
# from sql_models import create_table
# from sql_models.db_config import BaseType, PBaseModel
# from sqlalchemy import or_
#
#
# # id
# # job_name 任务名
# # created_time 创建时间
# # last_heartbeat    上次心跳时间
# # heartbeat_alarm    心跳断开时报警时间
# # alarm   超时未收到心跳时是否报警:0-否；1-是
# class TrackHeartbeat(PBaseModel):
#     __tablename__ = 'heartbeat'
#
#     jobname = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False)
#     url = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False)
#     alliance_uuid = BaseType.BaseColumn(BaseType.BaseString(588), nullable=False, default=uuid.uuid1)
#     created_time = BaseType.BaseColumn(BaseType.BaseDateTime, nullable=False, default=datetime.datetime.now)
#
#
# if __name__ == '__main__':
#     create_table()
