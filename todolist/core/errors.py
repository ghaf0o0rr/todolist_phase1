class ValidationError(Exception):
    pass

class DuplicateNameError(ValidationError):
    pass

class NotFoundError(Exception):
    pass

class LimitExceededError(Exception):
    pass
