from core.exceptions import CustomException 
 
 
class MenuDuplicateException(CustomException): 
    code = 400 
    error_code = 25000 
    message = "duplicate menu name" 
 
 
class MenuNotFoundException(CustomException): 
    code = 404 
    error_code = 25001 
    message = "menu not found" 
