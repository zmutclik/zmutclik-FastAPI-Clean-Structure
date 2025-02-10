from core.exceptions import DuplicateValueException, NotFoundException, BadRequestException
 
 
class UserDuplicateValueException(DuplicateValueException): 
    message = "duplicate akun name" 
 
 
class UserNotFoundException(NotFoundException): 
    message = "akun not found" 
    
class PasswordNotMatchException(BadRequestException): 
    message = "password does not match" 
