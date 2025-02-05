from core.exceptions import CustomException
from http import HTTPStatus


class DatabaseSavingException(CustomException):
    code = HTTPStatus.NOT_IMPLEMENTED
    error_code = HTTPStatus.NOT_IMPLEMENTED
    message = "database error saving"


class DatabaseUpdatingException(CustomException):
    code = HTTPStatus.NOT_IMPLEMENTED
    error_code = HTTPStatus.NOT_IMPLEMENTED
    message = "database error updating"

class DatabaseDeletingException(CustomException):
    code = HTTPStatus.NOT_IMPLEMENTED
    error_code = HTTPStatus.NOT_IMPLEMENTED
    message = "database error deleting"
