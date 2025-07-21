from typing import Any
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from user.application.exception import DuplicateEmailError
from user.interface.exception_handler import (
    duplicate_email_handler,
    validation_exception_handler,
)

from user.interface.controllers.user_controller import router as user_routers

app: Any = FastAPI()
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)
app.add_exception_handler(
    DuplicateEmailError,
    duplicate_email_handler,
)
app.include_router(user_routers)


@app.get("/")
def hello():
    return {"Hello": "FastAPI"}
