from core.exceptions import CustomException


class DatabaseSavingException(CustomException):
    code = 400
    error_code = 10101
    message = "database error saving"


class DatabaseUpdatingException(CustomException):
    code = 400
    error_code = 10102
    message = "database error updating"

class DatabaseDeletingException(CustomException):
    code = 400
    error_code = 10103
    message = "database error deleting"
