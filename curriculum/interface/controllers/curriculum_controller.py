from typing import Annotated
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from DI.containers import Container
from common.auth import CurrentUser, get_current_user
from curriculum.application.curriculum_service import CurriculumService
from curriculum.domain.value_object.visibility import Visibility
from curriculum.interface.schemas.curriculum_schema import (
    CreateCurriculumRequest,
    CreateCurriculumResponse,
    CreateLessonRequest,
    CreateWeekScheduleRequest,
    GenerateCurriculumRequest,
    GetCurriculumDetailResponse,
    GetCurriculumsPageResponse,
    UpdateCurriculumRequest,
    UpdateLessonsRequest,
)


router = APIRouter(prefix="/curriculums", tags=["Curriculums"])


@router.post("/", response_model=CreateCurriculumResponse, status_code=201)
@inject
async def create_curriculum_manual(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    request_body: CreateCurriculumRequest,
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
) -> CreateCurriculumResponse:
    new_manual_curriculum = await curriculum_service.create_curriculum(
        owner_id=current_user.id,
        title=request_body.title,
        week_schedules=[
            (
                week_schedule.week_number,
                week_schedule.lessons,
            )
            for week_schedule in request_body.week_schedules
        ],
        visibility=Visibility(request_body.visibility.value),
    )
    return CreateCurriculumResponse.from_domain(new_manual_curriculum)


@router.post("/generate", response_model=CreateCurriculumResponse, status_code=201)
@inject
async def create_curriculum_automatic(
    request_body: GenerateCurriculumRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
) -> CreateCurriculumResponse:
    print("▶▶▶ ENTER create_curriculum_automatic")
    curriculum = await curriculum_service.generate_curriculum(
        owner_id=current_user.id,
        goal=request_body.goal,
        period_weeks=request_body.period,
        difficulty=request_body.difficulty,
        details=request_body.details,
    )
    return CreateCurriculumResponse.from_domain(curriculum)


@router.get("/", response_model=GetCurriculumsPageResponse, status_code=200)
@inject
async def get_my_curriculums(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    page: int = 1,
    items_per_page: int = 10,
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    total_count, curriculums = await curriculum_service.get_curriculums(
        owner_id=current_user.id,
        role=current_user.role,
        page=page,
        items_per_page=items_per_page,
    )
    return GetCurriculumsPageResponse.from_domain(total_count, curriculums)


@router.get(
    "/{curriculum_id}",
    response_model=GetCurriculumDetailResponse,
    status_code=200,
)
@inject
async def get_curriculum_mine_public(
    curriculum_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
) -> GetCurriculumDetailResponse:
    curriculum_brief = await curriculum_service.get_curriculum_by_id(
        curriculum_id=curriculum_id,
        owner_id=current_user.id,
        role=current_user.role,
    )
    return GetCurriculumDetailResponse.from_domain(curriculum_brief)


@router.patch(
    "/{curriculum_id}",
    response_model=GetCurriculumDetailResponse,
    status_code=200,
)
@inject
async def update_curriculum(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    curriculum_id: str,
    request_body: UpdateCurriculumRequest,
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
) -> GetCurriculumDetailResponse:
    updated = await curriculum_service.update_curriculum(
        curriculum_id=curriculum_id,
        owner_id=current_user.id,
        role=current_user.role,
        title=request_body.title,
        visibility=request_body.visibility,
    )
    return GetCurriculumDetailResponse.from_domain(updated)


@router.delete("/{curriculum_id}", status_code=204)
@inject
async def delete_curriculum(
    curriculum_id: str,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    await curriculum_service.delete_curriculum(
        id=curriculum_id,
        owner_id=current_user.id,
        role=current_user.role,
    )


@router.post(
    "/{curriculum_id}/weeks",
    response_model=GetCurriculumDetailResponse,
    status_code=201,
)
@inject
async def create_week_schedule(
    curriculum_id: str,
    request_body: CreateWeekScheduleRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
) -> GetCurriculumDetailResponse:
    updated = await curriculum_service.create_week_schedule(
        curriculum_id=curriculum_id,
        owner_id=current_user.id,
        role=current_user.role,
        week_number=request_body.week_number,
        lessons=request_body.lessons,
    )
    return GetCurriculumDetailResponse.from_domain(updated)


@router.delete("/{curriculum_id}/weeks/{week_number}", status_code=204)
@inject
async def delete_week(
    curriculum_id: str,
    week_number: int,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):

    await curriculum_service.delete_week(
        curriculum_id=curriculum_id,
        owner_id=current_user.id,
        role=current_user.role,
        week_number=week_number,
    )


@router.post(
    "/{curriculum_id}/weeks/{week_number}/lessons",
    response_model=GetCurriculumDetailResponse,
    status_code=201,
)
@inject
async def create_lesson(
    curriculum_id: str,
    week_number: int,
    request_body: CreateLessonRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    updated = await curriculum_service.create_lesson(
        curriculum_id=curriculum_id,
        owner_id=current_user.id,
        role=current_user.role,
        week_number=week_number,
        lesson=request_body.lesson,
        lesson_index=request_body.index,
    )
    return GetCurriculumDetailResponse.from_domain(updated)


@router.patch(
    "/{curriculum_id}/weeks/{week_number}/lessons/{lesson_index}",
    status_code=200,
)
@inject
async def update_lesson(
    curriculum_id: str,
    week_number: int,
    lesson_index: int,
    request_body: UpdateLessonsRequest,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    print(f"[PATCH-IN] lesson_index={lesson_index}, payload={request_body}")
    updated_curriculum = await curriculum_service.update_lesson(
        curriculum_id=curriculum_id,
        owner_id=current_user.id,
        role=current_user.role,
        week_number=week_number,
        lesson_index=lesson_index,
        new_lesson=request_body.lesson,
    )

    return GetCurriculumDetailResponse.from_domain(updated_curriculum)


@router.delete(
    "/{curriculum_id}/weeks/{week_number}/lessons/{lesson_index}", status_code=204
)
@inject
async def delete_lesson(
    curriculum_id: str,
    week_number: int,
    lesson_index: int,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    curriculum_service: CurriculumService = Depends(
        Provide[Container.curriculum_service]
    ),
):
    await curriculum_service.delete_lesson(
        curriculum_id=curriculum_id,
        owner_id=current_user.id,
        role=current_user.role,
        week_number=week_number,
        lesson_index=lesson_index,
    )
