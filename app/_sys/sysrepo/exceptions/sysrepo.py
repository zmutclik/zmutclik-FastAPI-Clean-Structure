from core.exceptions import CustomException


class SysRepoDuplicateException(CustomException):
    code = 400
    error_code = 10200
    message = "duplicate name at this allocation is use "
    
    
class SysRepoNotFoundException(CustomException):
    code = 404
    error_code = 10201
    message = "sysrepo not found"
