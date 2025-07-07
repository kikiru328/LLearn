"""health check api"""

from datetime import datetime
import platform
import sys
from typing import Any, Dict
from fastapi import APIRouter, status


router = APIRouter(prefix="/health", tags=["Health Check"])


@router.get("", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, Any]:
    """
    Basic Health Check
    Is System work properly?
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "LLearn API",
        "version": "1.0.0",
    }


@router.get("/detailed", status_code=status.HTTP_200_OK)
async def detailed_health_check() -> Dict[str, Any]:
    """
    End point for detail health check
    system info with dependency status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": {
            "name": "LLearn API",
            "version": "1.0.0",
            "environment": "development",  # TODO: 환경 설정에서 가져오기
        },
        "system": {
            "platform": platform.system(),
            "python_version": sys.version,
            "architecture": platform.machine(),
        },
        "dependencies": {
            "database": "connected",  # TODO: 실제 DB 연결 상태 확인
            "llm_service": "available",  # TODO: 실제 LLM 서비스 상태 확인
        },
    }
