from fastapi import FastAPI
from app.api.v1.router import v1_router
from app.core.di_container import Container


class App(FastAPI):
    container: Container


app = App()
app.container = Container()
app.include_router(v1_router)


@app.get("/")
def hello() -> dict[str, str]:
    return {
        "message": "Curriculum Learning Platform API",
        "version": "1.0.0",
        "status": "running",
    }
