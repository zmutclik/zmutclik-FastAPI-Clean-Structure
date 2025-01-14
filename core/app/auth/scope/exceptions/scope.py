from core.exceptions import CustomException


class ScopeDuplicateException(CustomException):
    code = 400
    error_code = 23000
    message = "duplicate scope name"


class ScopeNotFoundException(CustomException):
    code = 404
    error_code = 23001
    message = "scope not found"
