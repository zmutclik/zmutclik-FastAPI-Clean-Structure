from core.exceptions import DuplicateValueException, NotFoundException, BadRequestException
 
 
class UserDuplicateValueException(DuplicateValueException): 
    message = "duplicate scope name" 
 
 
class UserNotFoundException(NotFoundException): 
    message = "scope not found" 
    
class PasswordNotMatchException(BadRequestException): 
    message = "password does not match" 
