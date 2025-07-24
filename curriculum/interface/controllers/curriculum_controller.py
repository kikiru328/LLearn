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
            content=str(summary.content),
            submitted_at=summary.submitted_at,
        )
        for summary in summaries
    ]


@router.post(
    "/{curriculum_id}/weeks/{week}/feedbacks",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def provide_feedback(
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
            comment=str(feedback.comment),
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
            comment=str(feedback.comment),
            score=feedback.score.value,
            created_at=feedback.created_at,
        )
        for feedback in feedbacks
    ]
