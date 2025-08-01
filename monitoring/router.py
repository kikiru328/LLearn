from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Monitoring"])


@router.get("/metrics")
async def get_metrics():
    """Prometheus 메트릭 엔드포인트"""
    try:
        metrics_data = generate_latest()
        return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)
    except Exception as e:
        logger.error(f"Error generating metrics: {e}")
        return Response(
            content="# Error generating metrics\n",
            media_type=CONTENT_TYPE_LATEST,
            status_code=500,
        )


@router.get("/health")
async def health_check():
    """애플리케이션 헬스체크"""
    return {"status": "healthy", "service": "curriculum-api", "version": "1.0.0"}
