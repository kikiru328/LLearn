from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.router import v1_router
from app.core.di_container import Container
from app.common.cache.redis_client import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 Redis 연결
    await redis_client.connect()
    yield
    # 종료 시 Redis 연결 해제
    await redis_client.disconnect()


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
