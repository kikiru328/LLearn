from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from curriculum.application.exception import (
    CurriculumNotFoundError,
    WeekScheduleNotFoundError,
    SummaryNotFoundError,
)


async def curriculum_not_found_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, CurriculumNotFoundError):
        return JSONResponse(
            status_code=204,
            content={"detail": "커리큘럼이 존재하지 않습니다."},
        )
    raise exc


async def week_schdule_not_found_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, WeekScheduleNotFoundError):
        return JSONResponse(
            status_code=204,
            content={"detail": "해당 주차의 커리큘럼이 존재하지 않습니다."},
        )
    raise exc


async def summary_not_found_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, SummaryNotFoundError):
        return JSONResponse(
            status_code=204,
            content={"detail": "요약본이 존재하지 않습니다."},
        )
    raise exc


def register_curriculum_exception_handlers(app: FastAPI):
    app.add_exception_handler(CurriculumNotFoundError, curriculum_not_found_handler)
    app.add_exception_handler(WeekScheduleNotFoundError, week_schdule_not_found_handler)
    app.add_exception_handler(SummaryNotFoundError, week_schdule_not_found_handler)
