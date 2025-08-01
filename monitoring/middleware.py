import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import logging

from monitoring.metrics import http_requests_total, http_request_duration

logger = logging.getLogger(__name__)


class PrometheusMiddleware(BaseHTTPMiddleware):
    """
    Prometheus 메트릭을 수집하는 FastAPI 미들웨어
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        # 요청 시작 시간 기록
        start_time = time.time()

        # 메트릭에서 제외할 경로들
        excluded_paths = ["/metrics", "/health", "/docs", "/redoc", "/openapi.json"]

        method = request.method
        path = request.url.path

        # 제외 경로는 메트릭 수집하지 않음
        if any(path.startswith(excluded) for excluded in excluded_paths):
            return await call_next(request)

        # 경로 정규화 (ID 파라미터를 일반화)
        normalized_path = self._normalize_path(path)

        try:
            # 요청 처리
            response = await call_next(request)
            status_code = str(response.status_code)

        except Exception as e:
            # 예외 발생 시 500으로 처리
            status_code = "500"
            logger.error(f"Request failed: {method} {path} - {e}")
            raise

        finally:
            # 응답 시간 계산
            duration = time.time() - start_time

            # 메트릭 업데이트
            http_requests_total.labels(
                method=method, endpoint=normalized_path, status_code=status_code
            ).inc()

            http_request_duration.labels(
                method=method, endpoint=normalized_path
            ).observe(duration)

        return response

    def _normalize_path(self, path: str) -> str:
        """
        경로를 정규화하여 메트릭 카디널리티를 줄임
        예: /api/v1/curriculums/abc123 -> /api/v1/curriculums/{id}
        """
        # API 경로 패턴 매핑
        path_patterns = {
            # User endpoints
            r"/api/v1/users/[^/]+$": "/api/v1/users/{username}",
            r"/api/v1/admins/[^/]+$": "/api/v1/admins/{username}",
            # Curriculum endpoints
            r"/api/v1/curriculums/[^/]+$": "/api/v1/curriculums/{id}",
            r"/api/v1/curriculums/[^/]+/weeks/\d+$": "/api/v1/curriculums/{id}/weeks/{week}",
            r"/api/v1/curriculums/[^/]+/weeks/\d+/lessons$": "/api/v1/curriculums/{id}/weeks/{week}/lessons",
            r"/api/v1/curriculums/[^/]+/weeks/\d+/lessons/\d+$": "/api/v1/curriculums/{id}/weeks/{week}/lessons/{index}",
            r"/api/v1/curriculums/[^/]+/weeks/\d+/summaries$": "/api/v1/curriculums/{id}/weeks/{week}/summaries",
            r"/api/v1/curriculums/[^/]+/weeks/\d+/summaries/[^/]+$": "/api/v1/curriculums/{id}/weeks/{week}/summaries/{summary_id}",
            r"/api/v1/curriculums/[^/]+/weeks/\d+/summaries/[^/]+/feedback$": "/api/v1/curriculums/{id}/weeks/{week}/summaries/{summary_id}/feedback",
            # Social endpoints
            r"/api/v1/curriculums/[^/]+/like$": "/api/v1/curriculums/{id}/like",
            r"/api/v1/curriculums/[^/]+/bookmark$": "/api/v1/curriculums/{id}/bookmark",
            r"/api/v1/curriculums/[^/]+/likes$": "/api/v1/curriculums/{id}/likes",
            r"/api/v1/curriculums/[^/]+/social-info$": "/api/v1/curriculums/{id}/social-info",
            # Comment endpoints
            r"/api/v1/curriculums/[^/]+/comments$": "/api/v1/curriculums/{id}/comments",
            r"/api/v1/curriculums/[^/]+/comments/stats$": "/api/v1/curriculums/{id}/comments/stats",
            r"/api/v1/curriculums/comments/[^/]+/replies$": "/api/v1/curriculums/comments/{id}/replies",
            r"/api/v1/curriculums/comments/[^/]+$": "/api/v1/curriculums/comments/{id}",
            # Admin endpoints
            r"/api/v1/admins/curriculums/[^/]+$": "/api/v1/admins/curriculums/{id}",
            r"/api/v1/admins/summaries/[^/]+$": "/api/v1/admins/summaries/{id}",
            r"/api/v1/admins/feedbacks/[^/]+$": "/api/v1/admins/feedbacks/{id}",
        }

        import re

        for pattern, replacement in path_patterns.items():
            if re.match(pattern, path):
                return replacement

        return path


class HealthCheckMiddleware(BaseHTTPMiddleware):
    """
    헬스체크 엔드포인트를 제공하는 미들웨어
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path == "/health":
            return Response(
                content='{"status": "healthy", "timestamp": "'
                + str(time.time())
                + '"}',
                media_type="application/json",
            )

        return await call_next(request)
