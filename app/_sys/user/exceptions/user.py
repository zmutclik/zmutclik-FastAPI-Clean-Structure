from core.exceptions import CustomException


class PasswordDoesNotMatchException(CustomException):
    code = 401
    error_code = 20000
    message = "password does not match"


class DuplicateEmailOrNicknameOrNoHPException(CustomException):
    code = 400
    error_code = 20001
    message = "duplicate email or nickname or nohp is use"


class UserNotFoundException(CustomException):
    code = 404
    error_code = 20002
    message = "user not found"
