from core.exceptions import CustomException 
 
 
class MenuTypeDuplicateException(CustomException): 
    code = 400 
    error_code = 24000 
    message = "duplicate menutype name" 
 
 
class MenuTypeNotFoundException(CustomException): 
    code = 404 
    error_code = 24001 
    message = "menutype not found" 
