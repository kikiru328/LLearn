from typing import Any
from fastapi import FastAPI
from DI.containers import Container

from user.interface.exception_handler import user_exceptions_handlers

from curriculum.interface.exception_handler import curriculum_exceptions_handlers
from api.v1.routers import v1_router


container = Container()
app: Any = FastAPI()
app.container = container
app.include_router(v1_router)

user_exceptions_handlers(app)
curriculum_exceptions_handlers(app)


@app.get("/")
def hello():
    return {"Hello": "FastAPI"}
