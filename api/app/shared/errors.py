class ExpiredRowVersionError(Exception):
    pass


class PlanInvalidError(Exception):
    pass


class AppValidationError(Exception):
    pass


class RowNotFoundError(Exception):
    pass
