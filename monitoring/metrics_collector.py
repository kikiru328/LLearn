import asyncio
import time
import logging
from typing import Optional
from dependency_injector.wiring import inject, Provide

from user.application.user_service import UserService
from curriculum.application.curriculum_service import CurriculumService
from curriculum.application.summary_service import SummaryService
from curriculum.application.feedback_service import FeedbackService
from curriculum.application.social_service import SocialService
from curriculum.application.comment_service import CommentService

from monitoring.metrics import (
    update_total_counts,
    app_start_time,
    app_info,
    db_connections_active,
)
from common.auth import Role
from user.domain.value_object.role import RoleVO

logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    주기적으로 비즈니스 메트릭을 수집하는 서비스
    """

    def __init__(
        self,
        user_service: UserService,
        curriculum_service: CurriculumService,
        summary_service: SummaryService,
        feedback_service: FeedbackService,
        social_service: Optional[SocialService] = None,
        comment_service: Optional[CommentService] = None,
        collection_interval: int = 60,  # 60초마다 수집
    ):
        self.user_service = user_service
        self.curriculum_service = curriculum_service
        self.summary_service = summary_service
        self.feedback_service = feedback_service
        self.social_service = social_service
        self.comment_service = comment_service
        self.collection_interval = collection_interval
        self._running = False
        self._task: Optional[asyncio.Task] = None

        # 애플리케이션 정보 설정
        app_info.info(
            {
                "version": "1.0.0",
                "environment": "development",  # 환경변수에서 가져오도록 수정 가능
                "python_version": "3.11+",
            }
        )

        # 애플리케이션 시작 시간 설정
        app_start_time.set(time.time())

    async def start_collection(self):
        """메트릭 수집 시작"""
        if self._running:
            logger.warning("Metrics collection is already running")
            return

        self._running = True
        self._task = asyncio.create_task(self._collection_loop())
        logger.info(
            f"Started metrics collection with {self.collection_interval}s interval"
        )

    async def stop_collection(self):
        """메트릭 수집 중지"""
        if not self._running:
            return

        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped metrics collection")

    async def _collection_loop(self):
        """메트릭 수집 루프"""
        while self._running:
            try:
                await self._collect_all_metrics()
                await asyncio.sleep(self.collection_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error during metrics collection: {e}")
                await asyncio.sleep(self.collection_interval)

    async def _collect_all_metrics(self):
        """모든 메트릭 수집"""
        try:
            # 사용자 통계
            total_users, _ = await self.user_service.get_users(page=1, items_per_page=1)

            # 커리큘럼 통계
            total_curriculums, curriculums = (
                await self.curriculum_service.get_curriculums(
                    owner_id=None,
                    role=RoleVO.ADMIN,
                    page=1,
                    items_per_page=1000,  # 공개 커리큘럼 수를 세기 위해 큰 수로 설정
                )
            )

            # 공개 커리큘럼 수 계산
            public_curriculums_count = sum(
                1
                for curriculum in curriculums
                if curriculum.visibility.value == "PUBLIC"
            )

            # 요약 통계
            total_summaries = await self.summary_service.get_total_summaries_count()

            # 피드백 통계
            total_feedbacks = await self.feedback_service.get_total_feedbacks_count()

            # 메트릭 업데이트
            update_total_counts(
                total_users=total_users,
                total_curriculums=total_curriculums,
                total_public_curriculums=public_curriculums_count,
                total_summaries=total_summaries,
                total_feedbacks=total_feedbacks,
            )

            logger.debug(
                f"Collected metrics - Users: {total_users}, Curriculums: {total_curriculums}, Summaries: {total_summaries}, Feedbacks: {total_feedbacks}"
            )

        except Exception as e:
            logger.error(f"Error collecting business metrics: {e}")

    async def collect_social_metrics(self):
        """소셜 메트릭 수집 (선택적)"""
        if not self.social_service:
            return

        try:
            # 여기에 소셜 메트릭 수집 로직 추가
            # 예: 총 좋아요 수, 북마크 수 등
            pass
        except Exception as e:
            logger.error(f"Error collecting social metrics: {e}")

    async def collect_comment_metrics(self):
        """댓글 메트릭 수집 (선택적)"""
        if not self.comment_service:
            return

        try:
            # 여기에 댓글 메트릭 수집 로직 추가
            pass
        except Exception as e:
            logger.error(f"Error collecting comment metrics: {e}")

    def get_current_stats(self) -> dict:
        """현재 통계 반환 (디버깅용)"""
        from prometheus_client import REGISTRY

        stats = {}
        for collector in REGISTRY._collector_to_names:
            for metric in collector.collect():
                stats[metric.name] = {
                    "help": metric.help,
                    "type": metric.type,
                    "samples": len(metric.samples) if hasattr(metric, "samples") else 0,
                }

        return stats


# 전역 메트릭 컬렉터 인스턴스
_metrics_collector: Optional[MetricsCollector] = None


@inject
async def initialize_metrics_collector(
    user_service: UserService = Provide["user_service"],
    curriculum_service: CurriculumService = Provide["curriculum_service"],
    summary_service: SummaryService = Provide["summary_service"],
    feedback_service: FeedbackService = Provide["feedback_service"],
    social_service: Optional[SocialService] = Provide["social_service"],
    comment_service: Optional[CommentService] = Provide["comment_service"],
):
    """메트릭 컬렉터 초기화"""
    global _metrics_collector

    if _metrics_collector is not None:
        logger.warning("Metrics collector already initialized")
        return _metrics_collector

    _metrics_collector = MetricsCollector(
        user_service=user_service,
        curriculum_service=curriculum_service,
        summary_service=summary_service,
        feedback_service=feedback_service,
        social_service=social_service,
        comment_service=comment_service,
    )

    await _metrics_collector.start_collection()
    logger.info("Metrics collector initialized and started")
    return _metrics_collector


async def shutdown_metrics_collector():
    """메트릭 컬렉터 종료"""
    global _metrics_collector

    if _metrics_collector:
        await _metrics_collector.stop_collection()
        _metrics_collector = None
        logger.info("Metrics collector shutdown complete")


def get_metrics_collector() -> Optional[MetricsCollector]:
    """현재 메트릭 컬렉터 인스턴스 반환"""
    return _metrics_collector
