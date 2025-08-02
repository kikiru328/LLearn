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


class TagNotFoundError(Exception):
    pass


class CategoryNotFoundError(Exception):
    pass


class DuplicateTagError(Exception):
    pass


class DuplicateCategoryError(Exception):
    pass
