from enum import StrEnum
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

from curriculum.domain.entity.curriculum import Curriculum


class VisibilityEnum(StrEnum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class WeekScheduleItem(BaseModel):
    week_number: int = Field(ge=1, description="주차 번호 (1~)")
    lessons: List[str] = Field(min_items=1, description="해당 주차의 학습 목록")


class CreateCurriculumRequest(BaseModel):
    title: str = Field(min_length=2, max_length=50, description="커리큘럼 제목")
    week_schedules: List[WeekScheduleItem] = Field(
        description="주차별 학습 스케쥴 목록"
    )
    visibility: VisibilityEnum = Field(
        default=VisibilityEnum.PRIVATE,
        description="커리큘럼 공개 여부 (Public or Private)",
    )


class CreateCurriculumResponse(BaseModel):
    id: str
    title: str
    visibility: VisibilityEnum
    week_schedules: List[WeekScheduleItem]

    @classmethod
    def from_domain(cls, curriculum: Curriculum) -> "CreateCurriculumResponse":
        week_items = [
            WeekScheduleItem(
                week_number=ws.week_number.value,
                lessons=ws.lessons.items,
            )
            for ws in curriculum.week_schedules
        ]
        return cls(
            id=str(curriculum.id),
            title=str(curriculum.title),
            visibility=VisibilityEnum(curriculum.visibility.value),
            week_schedules=week_items,
        )


class UpdateCurriculumRequest(BaseModel):
    title: str | None = None
    visibility: VisibilityEnum = Field(
        default=VisibilityEnum.PRIVATE,
        description="커리큘럼 공개 여부 (Public or Private)",
    )


class GetCurriculumDetailResponse(BaseModel):
    id: str
    owner_name: str
    title: str
    week_schedules: List[WeekScheduleItem]
    visibility: VisibilityEnum

    @classmethod
    def from_domain(cls, curriculum: Curriculum) -> "GetCurriculumDetailResponse":
        week_schedule_items = [
            WeekScheduleItem(
                week_number=week_schedule.week_number.value,
                lessons=week_schedule.lessons.items,
            )
            for week_schedule in curriculum.week_schedules
        ]
        return cls(
            id=str(curriculum.id),
            owner_name=curriculum.owner_name,
            title=str(curriculum.title),
            week_schedules=week_schedule_items,
            visibility=VisibilityEnum(curriculum.visibility.value),
        )


class GetCurriculumBriefResponse(BaseModel):
    id: str
    title: str
    owner_name: str
    visibility: VisibilityEnum


class GetCurriculumsPageResponse(BaseModel):
    total_count: int
    curriculums: List[GetCurriculumBriefResponse]

    @classmethod
    def from_domain(
        cls,
        total_count: int,
        curriculums: List[Curriculum],
    ) -> "GetCurriculumsPageResponse":
        briefs = []
        for curriculum in curriculums:
            briefs.append(
                GetCurriculumBriefResponse(
                    id=str(curriculum.id),
                    title=str(curriculum.title),
                    owner_name=curriculum.owner_name,
                    visibility=VisibilityEnum(curriculum.visibility.value),
                )
            )
        return cls(
            total_count=total_count,
            curriculums=briefs,
        )


class CreateWeekScheduleRequest(BaseModel):
    week_number: int = Field(ge=1, description="삽입 할 주차 번호")
    lessons: List[str] = Field(min_items=1, description="해당 주차에 추가할 학습 목록")


class CreateLessonRequest(BaseModel):
    lesson: str
    index: Optional[int] = Field(
        None, ge=0, description="삽입할 위치 (0부터). 미지정 시 마지막에 추가"
    )


class UpdateLessonsRequest(BaseModel):
    lesson: str


class GenerateCurriculumRequest(BaseModel):
    goal: str = Field(min_length=5, description="학습 목표")
    period: int = Field(ge=1, le=24, description="학습기간 (주 단위, 1~24주)")
    difficulty: Literal["beginner", "intermediate", "expert"] = Field(
        description="난이도 초급, 중급, 고급"
    )
    details: str = Field(description="세부 요청 사항")
