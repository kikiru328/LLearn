import pytest
from app.core.di_container import Container
from app.utils.performance_monitor import memory_profile


@memory_profile
async def test_container_initialization():
    container = Container()
    return container


@memory_profile
async def test_service_creation_loop():
    container = Container()
    services = []
    for i in range(50):
        user_service = container.user_service()
        curriculum_service = container.curriculum_service()
        services.extend([user_service, curriculum_service])

    return len(services)
