from core.exceptions import DuplicateValueException, NotFoundException
 
 
class ScopeDuplicateValueException(DuplicateValueException): 
    message = "duplicate scope name" 
 
 
class ScopeNotFoundException(NotFoundException): 
    message = "scope not found" 
