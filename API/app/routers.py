# 一级router
from fastapi import APIRouter
from app.AccountManagement.Account.view import account_router
from app.Clerk.VoluumSiteId.view import voluum_router
from app.DocumentManagement.Documents.view import documents_router
from app.DocumentManagement.Recycle.view import recycle_router
from app.PersonnelManagement.Departments.view import departments_router
from app.PersonnelManagement.Roles.view import roles_router
from app.PersonnelManagement.Users.view import users_router

# =====注册二级路由=====
# ### AccountManagement


acc_man_router = APIRouter(prefix="/api/AccountManagement", tags=["AccountManagement"])
acc_man_router.include_router(account_router)

# ### Clerk
clerk_router = APIRouter(prefix="/api/Clerk", tags=["Clerk"])
clerk_router.include_router(voluum_router)

# ### DocumentManagement
doc_man_router = APIRouter(prefix="/api/DocumentManagement", tags=["DocumentManagement"])
doc_man_router.include_router(documents_router)
doc_man_router.include_router(recycle_router)

# ### PersonnelManagement
per_man_router = APIRouter(prefix="/api/PersonnelManagement", tags=["PersonnelManagement"])
per_man_router.include_router(departments_router)
per_man_router.include_router(roles_router)
per_man_router.include_router(users_router)
