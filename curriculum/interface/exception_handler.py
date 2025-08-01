from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from curriculum.application.exception import (
    CurriculumNotFoundError,
    FeedbackNotFoundError,
    SummaryNotFoundError,
    CurriculumCountOverError,
    WeekScheduleNotFoundError,
    WeekIndexOutOfRangeError,
    FeedbackAlreadyExistsError,
)


async def validation_exception_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.errors()},
        )
    raise exc


async def value_error_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, ValueError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )
    raise exc


async def curriculum_not_found_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, CurriculumNotFoundError):
        return JSONResponse(
            status_code=409, content={"detail": "해당 커리큘럼을 찾을 수 없습니다."}
        )
    raise exc


async def summary_not_found_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, SummaryNotFoundError):
        return JSONResponse(
            status_code=409, content={"detail": "해당 요약본을 찾을 수 없습니다."}
        )


async def feedback_not_found_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, FeedbackNotFoundError):
        return JSONResponse(
            status_code=409, content={"detail": "해당 피드백을 찾을 수 없습니다."}
        )


async def curriculum_count_over_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, CurriculumCountOverError):
        return JSONResponse(
            status_code=400,
            content={
                "detail": "커리큘럼이 10개가 넘었습니다. 하나를 지우고 생성사세요."
            },
        )


async def week_schedule_not_found_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, WeekScheduleNotFoundError):
        return JSONResponse(
            status_code=400,
            content={"detail": "해당 주차를 찾을 수 없습니다."},
        )


async def week_index_out_of_range_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, WeekIndexOutOfRangeError):
        return JSONResponse(
            status_code=400,
            content={"detail": "주차는 최대의 5개의 lessons을 가질 수 있습니다."},
        )


async def feedback_already_exist_handler(
    request: Request,
    exc: Exception,
):
    if isinstance(exc, FeedbackAlreadyExistsError):
        return JSONResponse(
            status_code=400,
            content={
                "detail": "해당 피드백은 이미 존재합니다. 한 요약당 하나의 피드백이 제공됩니다."
            },
        )


# register
def curriculum_exceptions_handlers(app: FastAPI):
    # pydantic
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    # VO
    app.add_exception_handler(ValueError, value_error_handler)
    # custom (usercase)
    app.add_exception_handler(CurriculumNotFoundError, curriculum_not_found_handler)
    app.add_exception_handler(SummaryNotFoundError, summary_not_found_handler)
    app.add_exception_handler(FeedbackNotFoundError, feedback_not_found_handler)
    app.add_exception_handler(CurriculumCountOverError, curriculum_count_over_handler)
    app.add_exception_handler(
        WeekScheduleNotFoundError, week_schedule_not_found_handler
    )
    app.add_exception_handler(WeekIndexOutOfRangeError, week_index_out_of_range_handler)
    app.add_exception_handler(
        FeedbackAlreadyExistsError, feedback_already_exist_handler
    )
