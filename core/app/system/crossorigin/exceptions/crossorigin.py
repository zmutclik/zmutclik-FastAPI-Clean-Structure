from core.exceptions import CustomException


class CrossOriginDuplicateException(CustomException):
    code = 400
    error_code = 10400
    message = "link already created"


class CrossOriginNotFoundException(CustomException):
    code = 404
    error_code = 10401
    message = "link origin not found"
