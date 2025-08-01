class CurriculumNotFoundError(Exception):
    pass


class SummaryNotFoundError(Exception):
    pass


class FeedbackNotFoundError(Exception):
    pass


class CurriculumCountOverError(Exception):
    pass


class WeekScheduleNotFoundError(Exception):
    pass


class WeekIndexOutOfRangeError(Exception):
    pass


class FeedbackAlreadyExistsError(Exception):
    pass


class CommentNotFoundError(Exception):
    pass


class CommentPermissionError(Exception):
    pass
