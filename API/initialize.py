"""初始化文件"""
from app.routers import acc_man_router, clerk_router, doc_man_router, per_man_router, server_man_router
from fastapi.middleware.cors import CORSMiddleware

from config import GlobalsConfig
from sql_models.db_config import create_eng


def init_app(app):
    init_middleware(app)
    init_db()
    init_routers(app)


def init_middleware(app):
    # =====跨域=====
    # allow_origins 允许的url列表
    # allow_methods 允许的请求方式
    # allow_headers 允许的请求头
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_db():
    create_eng(GlobalsConfig)


def init_routers(app):
    # =====注册一级路由=====
    app.include_router(acc_man_router)
    app.include_router(clerk_router)
    app.include_router(doc_man_router)
    app.include_router(per_man_router)
    app.include_router(server_man_router)
