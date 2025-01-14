from core.exceptions import CustomException


class PrivilegeDuplicateException(CustomException):
    code = 400
    error_code = 22000
    message = "duplicate privilege name"


class PrivilegeNotFoundException(CustomException):
    code = 404
    error_code = 22001
    message = "privilege not found"
