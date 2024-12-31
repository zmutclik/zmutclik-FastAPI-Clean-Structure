from core.exceptions import CustomException


class CLASSNAMEDuplicateException(CustomException):
    code = 400
    error_code = 10000
    message = "VARNAME already created"


class CLASSNAMENotFoundException(CustomException):
    code = 404
    error_code = 10000
    message = "VARNAME not found"
