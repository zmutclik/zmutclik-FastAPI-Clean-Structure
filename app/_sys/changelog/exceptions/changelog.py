from core.exceptions import CustomException


class ChangeLogDuplicateException(CustomException):
    code = 400
    error_code = 10200
    message = "duplicate version name is use "
    
    
class ChangeLogNotFoundException(CustomException):
    code = 404
    error_code = 10201
    message = "changelog not found"
