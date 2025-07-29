from fastapi import APIRouter
from user.interface.controllers.auth_controller import router as auth_router
from user.interface.controllers.user_controller import router as user_router
from curriculum.interface.controllers.curriculum_controller import (
    router as curriculum_router,
)
from admin.interface.controllers.admin_controller import router as admin_router

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(auth_router)
v1_router.include_router(admin_router)
v1_router.include_router(user_router)
v1_router.include_router(curriculum_router)
