from core.exceptions import CustomException


class CLASSNAMEDuplicateException(CustomException):
    code = 400
    error_code = 10000
    message = "duplicate VARNAME name"


class CLASSNAMENotFoundException(CustomException):
    code = 404
    error_code = 10000
    message = "VARNAME not found"
