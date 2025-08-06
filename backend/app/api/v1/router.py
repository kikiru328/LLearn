from fastapi import APIRouter
from app.modules.user.interface.controller.user_controller import router as user_router
from app.modules.user.interface.controller.auth_controller import router as auth_router
from app.modules.curriculum.interface.controller.curriculum_controller import (
    curriculum_router,
    week_router,
    lesson_router,
)

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(auth_router)
v1_router.include_router(user_router)
v1_router.include_router(curriculum_router)
v1_router.include_router(week_router)
v1_router.include_router(lesson_router)
