"""
DI container <-> FastAPI Depends bridge
Interface Adapter -> Usecase

- each function return each usecase
- create usecase instance by DI

"""

from typing import Annotated

from fastapi import Depends
from app.core.container import Container

from usecase.user.create_user import CreateUserUseCase
from usecase.user.login_user import LoginUserUseCase
from usecase.user.get_user_profile import GetUserProfileUseCase

from usecase.curriculum.generate_curriculum_preview import (
    GenerateCurriculumPreviewUseCase,
)
from usecase.curriculum.save_curriculum import SaveCurriculumUseCase
from usecase.curriculum.get_user_curriculums import GetUserCurriculumsUseCase
from usecase.curriculum.get_curriculum_detail import GetCurriculumDetailUseCase
from usecase.curriculum.get_week_topic import GetWeekTopicUseCase

from usecase.summary.create_summary import CreateSummaryUseCase
from usecase.summary.get_user_summaries import GetUserSummariesUseCase
from usecase.summary.get_summary_detail import GetSummaryDetailUseCase
from usecase.summary.get_week_summaries import GetWeekSummariesUseCase

from usecase.feedback.generate_feedback import GenerateFeedbackUseCase
from usecase.feedback.get_feedback import GetFeedbackUseCase
from usecase.feedback.get_user_feedbacks import GetUserFeedbacksUseCase

container = Container()


# Users
def get_create_user_usecase() -> CreateUserUseCase:
    """inject usecase dependency for signin"""
    return container.create_user_usecase()


def get_login_user_usecase() -> LoginUserUseCase:
    return container.login_user_usecase()


def get_user_profile_usecase() -> GetUserProfileUseCase:
    return container.get_user_profile_usecase()


# Curriculums
def get_generate_curriculum_preview_usecase() -> GenerateCurriculumPreviewUseCase:
    return container.generate_curriculum_preview_usecase()


def get_save_curriculum_usecase() -> SaveCurriculumUseCase:
    return container.save_curriculum_usecase()


def get_user_curriculums_usecase() -> GetUserCurriculumsUseCase:
    return container.get_user_curriculums_usecase()


def get_curriculum_detail_usecase() -> GetCurriculumDetailUseCase:
    return container.get_curriculum_detail_usecase()


def get_week_topic_usecase() -> GetWeekTopicUseCase:
    return container.get_week_topic_usecase()


# Summary
def get_create_summary_usecase() -> CreateSummaryUseCase:
    return container.create_summary_usecase()


def get_user_summaries_usecase() -> GetUserSummariesUseCase:
    return container.get_user_summaries_usecase()


def get_summary_detail_usecase() -> GetSummaryDetailUseCase:
    return container.get_summary_detail_usecase()


def get_week_summaries_usecase() -> GetWeekSummariesUseCase:
    return container.get_week_summaries_usecase()


# Feedback
def get_generate_feedback_usecase() -> GenerateFeedbackUseCase:
    return container.generate_feedback_usecase()


def get_feedback_usecase() -> GetFeedbackUseCase:
    return container.get_feedback_usecase()


def get_user_feedbacks_usecase() -> GetUserFeedbacksUseCase:
    return container.get_user_feedbacks_usecase()


CreateUserUseCaseDep = Annotated[CreateUserUseCase, Depends(get_create_user_usecase)]
LoginUserUseCaseDep = Annotated[LoginUserUseCase, Depends(get_login_user_usecase)]
GetUserProfileUseCaseDep = Annotated[
    GetUserProfileUseCase, Depends(get_user_profile_usecase)
]

GenerateCurriculumPreviewUseCaseDep = Annotated[
    GenerateCurriculumPreviewUseCase, Depends(get_generate_curriculum_preview_usecase)
]
SaveCurriculumUseCaseDep = Annotated[
    SaveCurriculumUseCase, Depends(get_save_curriculum_usecase)
]
GetUserCurriculumsUseCaseDep = Annotated[
    GetUserCurriculumsUseCase, Depends(get_user_curriculums_usecase)
]
GetCurriculumDetailUseCaseDep = Annotated[
    GetCurriculumDetailUseCase, Depends(get_curriculum_detail_usecase)
]
GetWeekTopicUseCaseDep = Annotated[GetWeekTopicUseCase, Depends(get_week_topic_usecase)]

CreateSummaryUseCaseDep = Annotated[
    CreateSummaryUseCase, Depends(get_create_summary_usecase)
]
GetUserSummariesUseCaseDep = Annotated[
    GetUserSummariesUseCase, Depends(get_user_summaries_usecase)
]
GetSummaryDetailUseCaseDep = Annotated[
    GetSummaryDetailUseCase, Depends(get_summary_detail_usecase)
]
GetWeekSummariesUseCaseDep = Annotated[
    GetWeekSummariesUseCase, Depends(get_week_summaries_usecase)
]

GenerateFeedbackUseCaseDep = Annotated[
    GenerateFeedbackUseCase, Depends(get_generate_feedback_usecase)
]
GetFeedbackUseCaseDep = Annotated[GetFeedbackUseCase, Depends(get_feedback_usecase)]
GetUserFeedbacksUseCaseDep = Annotated[
    GetUserFeedbacksUseCase, Depends(get_user_feedbacks_usecase)
]
