from prometheus_client import Counter, Histogram, Gauge, Info
import time
from functools import wraps
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

# ========================= LLM 관련 메트릭 =========================

# LLM 요청 카운터
llm_requests_total = Counter(
    "llm_requests_total",
    "Total number of LLM requests",
    ["service", "model", "status"],  # curriculum_generation, feedback_generation
)

# LLM 응답 시간
llm_response_time = Histogram(
    "llm_response_time_seconds",
    "LLM response time in seconds",
    ["service", "model"],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, float("inf")),
)

# LLM 에러 카운터
llm_errors_total = Counter(
    "llm_errors_total", "Total number of LLM errors", ["service", "error_type"]
)

# ========================= API 성능 메트릭 =========================

# HTTP 요청 카운터
http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code"],
)

# HTTP 응답 시간
http_request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, float("inf")),
)

# ========================= 비즈니스 메트릭 =========================

# 사용자 활동
user_registrations_total = Counter(
    "user_registrations_total", "Total number of user registrations"
)
user_logins_total = Counter("user_logins_total", "Total number of user logins")
active_users_gauge = Gauge("active_users_total", "Number of currently active users")

# 커리큘럼 관련
curriculums_created_total = Counter(
    "curriculums_created_total",
    "Total number of curriculums created",
    ["type"],  # manual, generated
)
curriculums_total = Gauge("curriculums_total", "Total number of curriculums")
public_curriculums_total = Gauge(
    "public_curriculums_total", "Total number of public curriculums"
)

# 요약 및 피드백
summaries_created_total = Counter(
    "summaries_created_total", "Total number of summaries created"
)
feedbacks_created_total = Counter(
    "feedbacks_created_total", "Total number of feedbacks created"
)
summaries_total = Gauge("summaries_total", "Total number of summaries")
feedbacks_total = Gauge("feedbacks_total", "Total number of feedbacks")

# 소셜 활동
likes_total = Counter("likes_total", "Total number of likes")
bookmarks_total = Counter("bookmarks_total", "Total number of bookmarks")
comments_total = Counter("comments_total", "Total number of comments")

# ========================= 데이터베이스 메트릭 =========================

# DB 쿼리 성능
db_query_duration = Histogram(
    "db_query_duration_seconds",
    "Database query duration in seconds",
    ["operation", "table"],
    buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 2.0, float("inf")),
)

db_connections_active = Gauge(
    "db_connections_active", "Number of active database connections"
)

# ========================= 시스템 메트릭 =========================

# 애플리케이션 정보
app_info = Info("app_info", "Application information")
app_start_time = Gauge(
    "app_start_time_seconds", "Application start time in unix timestamp"
)

# ========================= 데코레이터 =========================


def track_llm_metrics(service: str, model: str = "gpt-4o"):
    """LLM 요청 메트릭 추적 데코레이터"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                llm_requests_total.labels(
                    service=service, model=model, status="success"
                ).inc()
                return result
            except Exception as e:
                llm_requests_total.labels(
                    service=service, model=model, status="error"
                ).inc()
                llm_errors_total.labels(
                    service=service, error_type=type(e).__name__
                ).inc()
                logger.error(f"LLM error in {service}: {e}")
                raise
            finally:
                duration = time.time() - start_time
                llm_response_time.labels(service=service, model=model).observe(duration)

        return wrapper

    return decorator


def track_db_metrics(operation: str, table: str):
    """데이터베이스 쿼리 메트릭 추적 데코레이터"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                duration = time.time() - start_time
                db_query_duration.labels(operation=operation, table=table).observe(
                    duration
                )

        return wrapper

    return decorator


# ========================= 메트릭 업데이트 함수 =========================


def increment_user_registration():
    """사용자 등록 메트릭 증가"""
    user_registrations_total.inc()


def increment_user_login():
    """사용자 로그인 메트릭 증가"""
    user_logins_total.inc()


def increment_curriculum_created(curriculum_type: str):
    """커리큘럼 생성 메트릭 증가"""
    curriculums_created_total.labels(type=curriculum_type).inc()


def increment_summary_created():
    """요약 생성 메트릭 증가"""
    summaries_created_total.inc()


def increment_feedback_created():
    """피드백 생성 메트릭 증가"""
    feedbacks_created_total.inc()


def increment_like():
    """좋아요 메트릭 증가"""
    likes_total.inc()


def increment_bookmark():
    """북마크 메트릭 증가"""
    bookmarks_total.inc()


def increment_comment():
    """댓글 메트릭 증가"""
    comments_total.inc()


# ========================= 게이지 업데이트 함수 =========================


def update_total_counts(
    total_users: int,
    total_curriculums: int,
    total_public_curriculums: int,
    total_summaries: int,
    total_feedbacks: int,
):
    """전체 카운트 게이지 업데이트"""
    active_users_gauge.set(total_users)
    curriculums_total.set(total_curriculums)
    public_curriculums_total.set(total_public_curriculums)
    summaries_total.set(total_summaries)
    feedbacks_total.set(total_feedbacks)
