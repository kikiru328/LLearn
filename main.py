from typing import Any
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from DI.containers import Container
from user.interface.exception_handler import user_exceptions_handlers
from curriculum.interface.exception_handler import curriculum_exceptions_handlers
from api.v1.routers import v1_router
from monitoring.endpoints import router as monitoring_router
from monitoring.middleware import PrometheusMiddleware, HealthCheckMiddleware
from monitoring.metrics_collector import (
    initialize_metrics_collector,
    shutdown_metrics_collector,
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 라이프사이클 관리"""
    # 시작 시
    logger.info("Starting application...")

    # DI 컨테이너 와이어링
    container = app.container
    container.wire(
        packages=[
            "user.interface.controllers",
            "curriculum.interface.controllers",
            "admin.interface.controllers",
            "monitoring",
        ]
    )

    # 메트릭 컬렉터 초기화
    try:
        await initialize_metrics_collector()
        logger.info("Metrics collector initialized")
    except Exception as e:
        logger.error(f"Failed to initialize metrics collector: {e}")

    logger.info("Application startup complete")

    yield

    # 종료 시
    logger.info("Shutting down application...")

    # 메트릭 컬렉터 종료
    try:
        await shutdown_metrics_collector()
        logger.info("Metrics collector shut down")
    except Exception as e:
        logger.error(f"Error shutting down metrics collector: {e}")

    logger.info("Application shutdown complete")


# FastAPI 앱 생성
app: Any = FastAPI(
    title="Curriculum Learning Platform API",
    description="A comprehensive learning platform with social features",
    version="1.0.0",
    lifespan=lifespan,
)

# DI 컨테이너 설정
container = Container()
app.container = container

# 미들웨어 추가 (순서 중요!)
app.add_middleware(PrometheusMiddleware)
app.add_middleware(HealthCheckMiddleware)

# 라우터 추가
app.include_router(v1_router)
app.include_router(monitoring_router)

# 예외 핸들러 등록
user_exceptions_handlers(app)
curriculum_exceptions_handlers(app)


@app.get("/")
def hello():
    return {
        "message": "Curriculum Learning Platform API",
        "version": "1.0.0",
        "status": "running",
    }
