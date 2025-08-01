from typing import Annotated, List
from fastapi import APIRouter, Depends, status, Query, Path
from dependency_injector.wiring import inject, Provide
from common.auth import get_current_user, CurrentUser

from curriculum.application.curriculum_service import CurriculumService
from curriculum.domain.entity.curriculum import Curriculum as CurriculumDomain

from curriculum.domain.value_object.feedback_comment import FeedbackComment
from curriculum.domain.value_object.feedback_score import FeedbackScore
from curriculum.domain.value_object.summary_content import SummaryContent
from curriculum.interface.schemas.curriculum_schema import (
    CurriculumGenerateRequest,
    CurriculumUpdateRequest,
    CurriculumResponse,
    PaginatedCurriculumsResponse,
    SummaryRequest,
    SummaryResponse,
    FeedbackRequest,
    FeedbackResponse,
    WeekScheduleBody,
)
from DI.containers import Container

router = APIRouter(prefix="/curriculums", tags=["curriculums"])


def _to_curriculum_response(domain: CurriculumDomain) -> CurriculumResponse:
    return CurriculumResponse(
        id=domain.id,
        owner_id=domain.owner_id,
        topic=str(domain.title),
        duration_weeks=domain.week_schedules.__len__(),  # or stored value
        week_schedules=[
            WeekScheduleBody(week_number=ws.week_number.value, topics=ws.topics.items)
            for ws in domain.week_schedules
        ],
        created_at=domain.created_at,
        updated_at=domain.updated_at,
    )


@router.post("", response_model=CurriculumResponse, status_code=status.HTTP_201_CREATED)
@inject
async def create_curriculum(
    request: CurriculumGenerateRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    domain = await curriculum_service.generate_and_create_curriculum(
        owner_id=current_user.id, goal=request.topic, weeks=request.duration_weeks
    )
    return _to_curriculum_response(domain)


@router.get(
    "/{curriculum_id}",
    response_model=CurriculumResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_curriculum(
    curriculum_id: str = Path(..., description="커리큘럼 ID (str)"),
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    domain = await curriculum_service.get_curriculum_by_id(curriculum_id)
    return _to_curriculum_response(domain)


@router.get(
    "", response_model=PaginatedCurriculumsResponse, status_code=status.HTTP_200_OK
)
@inject
async def list_curriculums(
    page: int = Query(1, ge=1),
    items_per_page: int = Query(10, ge=1, le=100),
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    total, domains = await curriculum_service.get_curriculums(page, items_per_page)
    return PaginatedCurriculumsResponse(
        total_count=total,
        page=page,
        items_per_page=items_per_page,
        curriculums=[_to_curriculum_response(d) for d in domains],
    )


@router.put(
    "/{curriculum_id}",
    response_model=CurriculumResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def update_curriculum(
    curriculum_id: str = Path(..., description="커리큘럼 ID (str)"),
    request: CurriculumUpdateRequest = Depends(),
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    updated = await curriculum_service.update_curriculum_title(
        curriculum_id, request.topic
    )
    return _to_curriculum_response(updated)


@router.delete(
    "/{curriculum_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_curriculum(
    curriculum_id: str = Path(..., description="커리큘럼 ID (str)"),
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    await curriculum_service.delete_curriculum(curriculum_id)


@router.delete(
    "/{curriculum_id}/weeks/{week}",
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_week_schedule(
    curriculum_id: str = Path(..., description="커리큘럼 ID"),
    week: int = Path(..., ge=1, description="주차 번호"),
    force: bool = Query(False, description="강제 삭제 여부"),
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    if not force:
        summaries = await curriculum_service.get_summaries_by_week(curriculum_id, week)
        feedbacks = await curriculum_service.get_feedbacks_by_week(curriculum_id, week)

        if summaries or feedbacks:
            return {
                "warning": f"주차 {week}에 요약 {len(summaries)}개, 피드백 {len(feedbacks)}개가 함께 삭제됩니다.",
                "require_force": True,
                "summary_count": len(summaries),
                "feedback_count": len(feedbacks),
            }

    await curriculum_service.delete_week_schedule(curriculum_id, week)
    return {"message": f"주차 {week} 삭제 완료"}


@router.post(
    "/{curriculum_id}/summaries",
    response_model=SummaryResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def submit_summary(
    curriculum_id: str = Path(..., description="커리큘럼 ID (str)"),
    body: SummaryRequest = Depends(),
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    summary = await curriculum_service.submit_summary(
        curriculum_id, body.week_number, SummaryContent(body.content)
    )
    return SummaryResponse(
        id=summary.id,
        content=str(summary.content),
        submitted_at=summary.submitted_at,
    )


@router.get(
    "/{curriculum_id}/summaries",
    response_model=List[SummaryResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_summaries(
    curriculum_id: str = Path(..., description="커리큘럼 ID (str)"),
    week: int = Query(..., ge=1),
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    summaries = await curriculum_service.get_summaries_by_week(curriculum_id, week)
    return [
        SummaryResponse(
            id=summary.id,
            content=summary.content.value,
            submitted_at=summary.submitted_at,
        )
        for summary in summaries
    ]


@router.delete(
    "/{curriculum_id}/summaries/{summary_id}",
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_summary(
    curriculum_id: str = Path(..., description="커리큘럼 ID"),
    summary_id: str = Path(..., description="요약 ID"),
    force: bool = Query(False, description="강제 삭제 여부"),
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    if not force:
        try:
            all_feedbacks = await curriculum_service.get_all_feedbacks(curriculum_id)
            related_feedbacks = [
                f
                for f in all_feedbacks
                if hasattr(f, "summary_id") and f.summary_id == summary_id
            ]

            if related_feedbacks:
                return {
                    "warning": f"요약에 연결된 피드백 {len(related_feedbacks)}개가 함께 삭제됩니다.",
                    "require_force": True,
                    "feedback_count": len(related_feedbacks),
                }
        except Exception:
            pass

    # 2) 삭제 실행 (피드백도 함께 삭제됨)
    await curriculum_service.delete_summary(summary_id)
    return {"message": f"요약 {summary_id} 삭제 완료"}


@router.post(
    "/{curriculum_id}/weeks/{week}/feedbacks-manuel",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def provide_feedback_by_manuel(
    curriculum_id: str = Path(..., description="커리큘럼 ID (str)"),
    week: int = Path(..., ge=1),
    body: FeedbackRequest = Depends(),
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    fb = await curriculum_service.provide_feedback(
        curriculum_id,
        week,
        body.summary_id,
        FeedbackComment(body.comment),
        FeedbackScore(body.score),
    )
    return FeedbackResponse(
        id=fb.id,
        comment=str(fb.comment),
        score=fb.score.value,
        created_at=fb.created_at,
    )


@router.post(
    "/{curriculum_id}/week/{week}/feedback-generate",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def submit_summary_with_auto_feedback(
    curriculum_id: str = Path(..., description="커리큘럼 ID"),
    week_number: int = Query(..., ge=1, description="주차 번호"),
    content: str = Query(..., min_length=300, description="요약 내용"),
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    summary_content = SummaryContent(content)
    summary, feedback = await curriculum_service.submit_summary_with_auto_feedback(
        curriculum_id, week_number, summary_content
    )

    return {
        "summary": {
            "id": summary.id,
            "content": summary.content.value,
            "submitted_at": summary.submitted_at,
        },
        "feedback": {
            "id": feedback.id,
            "comment": feedback.comment.value,
            "score": feedback.score.value,
            "created_at": feedback.created_at,
        },
    }


@router.get(
    "/{curriculum_id}/weeks/{week}/feedbacks",
    response_model=List[FeedbackResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_feedbacks_by_week(
    curriculum_id: str = Path(..., description="커리큘럼 ID (str)"),
    week: int = Path(..., ge=1),
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    feedbacks = await curriculum_service.get_feedbacks_by_week(curriculum_id, week)
    return [
        FeedbackResponse(
            id=feedback.id,
            comment=feedback.comment.value,
            score=feedback.score.value,
            created_at=feedback.created_at,
        )
        for feedback in feedbacks
    ]


@router.get(
    "/{curriculum_id}/feedbacks",
    response_model=List[FeedbackResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all_feedbacks(
    curriculum_id: str = Path(..., description="커리큘럼 ID (str)"),
    service: CurriculumService = Depends(Provide[Container.curriculum_service]),
):
    feedbacks = await service.get_all_feedbacks(curriculum_id)
    return [
        FeedbackResponse(
            id=feedback.id,
            comment=feedback.comment.value,
            score=feedback.score.value,
            created_at=feedback.created_at,
        )
        for feedback in feedbacks
    ]
