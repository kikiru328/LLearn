class CurriculumNotFoundError(Exception):
    pass


class WeekScheduleNotFoundError(Exception):
    """해당 커리큘럼에 지정된 주차 스케줄이 없을 때 발생합니다."""

    pass


class SummaryNotFoundError(Exception):
    pass
