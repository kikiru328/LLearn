from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from common.auth import CurrentUser, get_current_user
from curriculum.application.exception import FeedbackNotFoundError
from curriculum.application.feedback_service import FeedbackService
from curriculum.interface.schemas.feedback_schema import FeedbackResponse
from DI.containers import Container

router = APIRouter(
    prefix="/curriculums/{curriculum_id}/weeks/{week_number}/summaries/{summary_id}/feedback",
    tags=["Feedbacks"],
)


@router.post("/", response_model=FeedbackResponse, status_code=201)
@inject
async def create_feedback(
    curriculum_id: str,
    week_number: int,
    summary_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    feedback_service: FeedbackService = Depends(Provide[Container.feedback_service]),
):

    feedback = await feedback_service.create_feedback(
        owner_id=current_user.id,
        role=current_user.role,
        curriculum_id=curriculum_id,
        summary_id=summary_id,
    )
    return FeedbackResponse.from_domain(feedback)


@router.get("/", response_model=Optional[FeedbackResponse], status_code=200)
@inject
async def get_feedback(
    curriculum_id: str,
    week_number: int,
    summary_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    feedback_service: FeedbackService = Depends(Provide[Container.feedback_service]),
):

    feedback = await feedback_service.get_feedback(
        owner_id=current_user.id,
        role=current_user.role,
        curriculum_id=curriculum_id,
        summary_id=summary_id,
    )
    if not feedback:
        raise FeedbackNotFoundError("Feedback not found")
    return FeedbackResponse.from_domain(feedback)


@router.delete("/{feedback_id}", status_code=204)
@inject
async def delete_feedback(
    curriculum_id: str,
    week_number: int,
    summary_id: str,
    feedback_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    feedback_service: FeedbackService = Depends(Provide[Container.feedback_service]),
):
    await feedback_service.delete_feedback(
        owner_id=current_user.id,
        role=current_user.role,
        curriculum_id=curriculum_id,
        summary_id=summary_id,
        feedback_id=feedback_id,
    )
