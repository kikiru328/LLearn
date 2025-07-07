"""health check api"""

from datetime import datetime, timezone
import platform
import sys
from typing import Any, Dict
from fastapi import APIRouter, status

from app.core.config import settings
from app.schemas.health_check import (
    BasicHealthCheckResponse,
    DependencyStatus,
    DetailedHealthCheckResponse,
    ServiceInfo,
    SystemInfo,
)


router = APIRouter(prefix="/health", tags=["Health Check"])


@router.get("", status_code=status.HTTP_200_OK)
async def health_check() -> BasicHealthCheckResponse:
    """
    Basic Health Check
    Is System work properly?
    """
    return BasicHealthCheckResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        service=settings.service_name,
        version=settings.service_version,
    )


@router.get("/detailed", status_code=status.HTTP_200_OK)
async def detailed_health_check() -> DetailedHealthCheckResponse:
    """
    End point for detail health check
    system info with dependency status
    """
    return DetailedHealthCheckResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        service=ServiceInfo(
            name=settings.service_name,
            version=settings.service_version,
            environment=settings.environment,
        ),
        system=SystemInfo(
            platform=platform.system(),
            python_version=sys.version,
            architecture=platform.machine(),
        ),
        dependencies=DependencyStatus(
            database="connected",  # TODO: 실제 DB 연결 상태 확인
            llm_service="available",  # TODO: 실제 LLM 서비스 상태 확인
        ),
    )
