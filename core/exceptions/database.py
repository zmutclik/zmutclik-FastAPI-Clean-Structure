from core.exceptions import CustomException


class DatabaseSavingException(CustomException):
    code = 501
    message = "database error saving"


class DatabaseUpdatingException(CustomException):
    code = 501
    message = "database error updating"

class DatabaseDeletingException(CustomException):
    code = 501
    message = "database error deleting"
