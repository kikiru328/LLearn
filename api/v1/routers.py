from fastapi import APIRouter
from user.interface.controllers.auth_controller import router as auth_router
from user.interface.controllers.user_controller import router as user_router
from curriculum.interface.controllers.curriculum_controller import (
    router as curriculum_router,
)
from curriculum.interface.controllers.summary_controller import (
    router as summary_router,
    user_summary_router,
)
from curriculum.interface.controllers.feedback_controller import (
    router as feedback_router,
)
from admin.interface.controllers.admin_user_controller import (
    router as admin_user_router,
)
from admin.interface.controllers.admin_curriculum_controller import (
    router as admin_curriculum_controller,
)
from admin.interface.controllers.admin_summary_controller import (
    router as admin_summary_controller,
)

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(auth_router)
v1_router.include_router(admin_user_router)
v1_router.include_router(admin_curriculum_controller)
v1_router.include_router(admin_summary_controller)
v1_router.include_router(user_router)
v1_router.include_router(curriculum_router)
v1_router.include_router(user_summary_router)
v1_router.include_router(summary_router)
v1_router.include_router(feedback_router)
