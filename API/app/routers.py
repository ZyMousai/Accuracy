# 一级router
from fastapi import APIRouter
from app.AccountManagement.Account.view import account_router
from app.Clerk.Track.view import track_router
from app.Clerk.VoluumSiteId.view import voluum_router
from app.Clerk.Card.view import clerk_card_router
from app.Clerk.Scheduler.view import clerk_scheduler_router
from app.DocumentManagement.Documents.view import documents_router
from app.DocumentManagement.Recycle.view import recycle_router
from app.OffersSystem.Offers.view import offers_router
from app.OffersSystem.OffersAccount.view import offers_account_router
from app.OffersSystem.OffersUnion.view import offers_union_router
from app.PersonnelManagement.Departments.view import departments_router
from app.PersonnelManagement.Roles.view import roles_router
from app.PersonnelManagement.Users.view import users_router
from app.ServerManagenebt.ServerConfig.view import server_router

# =====注册二级路由=====
# ### AccountManagement
acc_man_router = APIRouter(prefix="/api/AccountManagement")
acc_man_router.include_router(account_router)

# ### Clerk
clerk_router = APIRouter(prefix="/api/Clerk")
clerk_router.include_router(voluum_router)
clerk_router.include_router(clerk_card_router)
clerk_router.include_router(track_router)
clerk_router.include_router(clerk_scheduler_router)

# ### DocumentManagement
doc_man_router = APIRouter(prefix="/api/DocumentManagement")
doc_man_router.include_router(documents_router)
doc_man_router.include_router(recycle_router)

# ### PersonnelManagement
per_man_router = APIRouter(prefix="/api/PersonnelManagement")
per_man_router.include_router(departments_router)
per_man_router.include_router(roles_router)
per_man_router.include_router(users_router)

# ### ServerManagement
server_man_router = APIRouter(prefix="/api/ServerManagement")
server_man_router.include_router(server_router)

# ### OffersSystem
offers_system_router = APIRouter(prefix="/api/OffersSystem")
offers_system_router.include_router(offers_account_router)
offers_system_router.include_router(offers_union_router)
offers_system_router.include_router(offers_router)
