from core.exceptions import DuplicateValueException, NotFoundException
 
 
class PrivilegeDuplicateValueException(DuplicateValueException): 
    message = "duplicate privilege name" 
 
 
class PrivilegeNotFoundException(NotFoundException): 
    message = "privilege not found" 
