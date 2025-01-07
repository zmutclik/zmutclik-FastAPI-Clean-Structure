from core.exceptions import CustomException


class PasswordDoesNotMatchException(CustomException):
    code = 401
    error_code = 21000
    message = "password does not match"


class DuplicateEmailOrNicknameOrNoHPException(CustomException):
    code = 400
    error_code = 21001
    message = "duplicate email or nickname or nohp is use"


class UserNotFoundException(CustomException):
    code = 404
    error_code = 21002
    message = "user not found"


class UserNotActiveException(CustomException):
    code = 400
    error_code = 21003
    message = "user has been is inactive"
