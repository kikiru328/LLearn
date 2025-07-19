from typing import Any
from fastapi import FastAPI

app: Any = FastAPI()


@app.get("/")
def hello():
    return {"Hello": "FastAPI"}
