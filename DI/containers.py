from dependency_injector import containers, providers

from config import get_settings

from curriculum.application.curriculum_service import CurriculumService
from curriculum.infra.repository.curriculum_repo import CurriculumRepository

from curriculum.application.summary_service import SummaryService
from curriculum.infra.repository.summary_repo import SummaryRepository

from curriculum.application.feedback_service import FeedbackService
from curriculum.infra.repository.feedback_repo import FeedbackRepository

from curriculum.infra.llm.openai_client import OpenAILLMClient

from curriculum.application.social_service import SocialService
from curriculum.infra.repository.like_repo import LikeRepository
from curriculum.infra.repository.bookmark_repo import BookmarkRepository

from curriculum.application.comment_service import CommentService
from curriculum.infra.repository.comment_repo import CommentRepository

from curriculum.infra.repository.category_repo import CategoryRepository
from curriculum.infra.repository.curriculum_tag_repo import (
    CurriculumTagRepository,
    CurriculumCategoryRepository,
)

from curriculum.infra.repository.tag_repo import TagRepository
from curriculum.application.tag_service import TagService


from db.database import AsyncSessionLocal
from user.application.auth_service import AuthService
from user.application.user_service import UserService
from user.infra.repository.user_repo import UserRepository
from ulid import ULID

from utils.crypto import Crypto


class Container(containers.DeclarativeContainer):
    # setting
    wiring_config = containers.WiringConfiguration(
        packages=[
            "user.interface.controllers",
            "curriculum.interface.controllers",
            "admin.interface.controllers",
            "monitoring",
        ]
    )

    config = providers.Singleton(get_settings)

    db_session = providers.Factory(AsyncSessionLocal)

    # LLM
    llm_client = providers.Singleton(
        OpenAILLMClient,
        api_key=config.provided.llm_api_key,
        endpoint=config.provided.llm_endpoint,
    )

    # User
    user_repository = providers.Factory(
        UserRepository,
        session=db_session,
    )

    user_service = providers.Factory(
        UserService,
        user_repo=user_repository,
        ulid=providers.Singleton(ULID),
        crypto=providers.Singleton(Crypto),
    )

    auth_service = providers.Factory(
        AuthService,
        user_repo=user_repository,
        ulid=providers.Singleton(ULID),
        crypto=providers.Singleton(Crypto),
    )

    # Curriculum
    curriculum_repository = providers.Factory(
        CurriculumRepository,
        session=db_session,
    )

    curriculum_service = providers.Factory(
        CurriculumService,
        curriculum_repo=curriculum_repository,
        llm_client=llm_client,
        ulid=providers.Singleton(ULID),
    )

    # Summary

    summary_repository = providers.Factory(
        SummaryRepository,
        session=db_session,
    )

    feedback_repository = providers.Factory(
        FeedbackRepository,
        session=db_session,
    )

    summary_service = providers.Factory(
        SummaryService,
        summary_repo=summary_repository,
        curriculum_repo=curriculum_repository,
        feedback_repo=feedback_repository,
        ulid=providers.Singleton(ULID),
    )

    # Feedback

    feedback_service = providers.Factory(
        FeedbackService,
        feedback_repo=feedback_repository,
        summary_repo=summary_repository,
        curriculum_repo=curriculum_repository,
        llm_client=llm_client,
        ulid=providers.Singleton(ULID),
    )

    # Social

    like_repository = providers.Factory(LikeRepository, session=db_session)
    bookmark_repository = providers.Factory(BookmarkRepository, session=db_session)

    social_service = providers.Factory(
        SocialService,
        like_repo=like_repository,
        bookmark_repo=bookmark_repository,
        curriculum_repo=curriculum_repository,
    )

    comment_repository = providers.Factory(CommentRepository, session=db_session)
    comment_service = providers.Factory(
        CommentService,
        comment_repo=comment_repository,
        curriculum_repo=curriculum_repository,
    )

    # Tag & Category

    category_repository = providers.Factory(
        CategoryRepository,
        session=db_session,
    )

    tag_repository = providers.Factory(
        TagRepository,
        session=db_session,
    )

    curriculum_tag_repository = providers.Factory(
        CurriculumTagRepository,
        session=db_session,
    )

    curriculum_category_repository = providers.Factory(
        CurriculumCategoryRepository,
        session=db_session,
    )

    # Tag Service
    tag_service = providers.Factory(
        TagService,
        category_repo=category_repository,
        tag_repo=tag_repository,
        curriculum_tag_repo=curriculum_tag_repository,
        curriculum_category_repo=curriculum_category_repository,
        curriculum_repo=curriculum_repository,
        ulid=providers.Singleton(ULID),
    )
