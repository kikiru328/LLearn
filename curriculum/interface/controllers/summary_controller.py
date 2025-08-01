from typing import Annotated
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from DI.containers import Container
from common.auth import CurrentUser, get_current_user
from curriculum.application.summary_service import SummaryService
from curriculum.interface.schemas.summary_schema import (
    CreateSummaryReqeust,
    SummaryDetailResponse,
    SummaryPageResponse,
)


router = APIRouter(
    prefix="/curriculums/{curriculum_id}/weeks/{week_number}/summaries",
    tags=["Summaries"],
)


@router.post("/", response_model=SummaryDetailResponse, status_code=201)
@inject
async def create_summary(
    curriculum_id: str,
    week_number: int,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    request_body: CreateSummaryReqeust,
    summary_service: SummaryService = Depends(Provide[Container.summary_service]),
):
    summary, feedback = await summary_service.create_summary(
        owner_id=current_user.id,
        role=current_user.role,
        curriculum_id=curriculum_id,
        week_number=week_number,
        content=request_body.content,
    )
    return SummaryDetailResponse.from_domain(summary, feedback)


@router.get("/", response_model=SummaryPageResponse, status_code=200)
@inject
async def get_summaries(
    curriculum_id: str,
    week_number: int,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    summary_service: SummaryService = Depends(Provide[Container.summary_service]),
    page: int = 1,
    items_per_page: int = 10,
):

    total_count, summaries = await summary_service.get_summaries(
        owner_id=current_user.id,
        role=current_user.role,
        curriculum_id=curriculum_id,
        week_number=week_number,
        page=page,
        items_per_page=items_per_page,
    )
    return SummaryPageResponse.from_domain(total_count, summaries)


@router.get("/{summary_id}", response_model=SummaryDetailResponse, status_code=200)
@inject
async def get_summary(
    curriculum_id: str,
    week_number: int,
    summary_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    summary_service: SummaryService = Depends(Provide[Container.summary_service]),
):

    summary, feedback = await summary_service.get_summary(
        owner_id=current_user.id,
        role=current_user.role,
        summary_id=summary_id,
    )
    return SummaryDetailResponse.from_domain(summary, feedback)


@router.delete("/{summary_id}", status_code=204)
@inject
async def delete_summary(
    curriculum_id: str,
    week_number: int,
    summary_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    summary_service: SummaryService = Depends(Provide[Container.summary_service]),
):

    await summary_service.delete_summary(
        owner_id=current_user.id,
        role=current_user.role,
        summary_id=summary_id,
    )


user_summary_router = APIRouter(prefix="/summaries", tags=["User Summaries"])


@user_summary_router.get(
    "/me",
    response_model=SummaryPageResponse,
    status_code=200,
)
@inject
async def get_my_summaries(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    summary_service: SummaryService = Depends(Provide[Container.summary_service]),
    page: int = 1,
    items_per_page: int = 10,
):
    total, summaries = await summary_service.get_my_summaries(
        owner_id=current_user.id,
        page=page,
        items_per_page=items_per_page,
    )
    return SummaryPageResponse.from_domain(total, summaries)
