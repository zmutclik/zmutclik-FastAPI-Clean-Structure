from core.exceptions import DuplicateValueException, NotFoundException 
 
 
class MenuTypeDuplicateException(DuplicateValueException): 
    message = "duplicate menutype name" 
 
 
class MenuTypeNotFoundException(NotFoundException): 
    message = "menutype not found" 
