from typing import Any
from fastapi import FastAPI
from DI.containers import Container
from curriculum.interface.exception_handler import (
    register_curriculum_exception_handlers,
)
from user.interface.exception_handler import register_user_exception_handlers

from user.interface.controllers.auth_controller import router as auth_routers
from user.interface.controllers.user_controller import router as user_routers
from curriculum.interface.controllers.curriculum_controller import (
    router as curriculum_routers,
)


container = Container()

app: Any = FastAPI()

app.container = container

register_user_exception_handlers(app)
register_curriculum_exception_handlers(app)

app.include_router(auth_routers)
app.include_router(user_routers)
app.include_router(curriculum_routers)


@app.get("/")
def hello():
    return {"Hello": "FastAPI"}
