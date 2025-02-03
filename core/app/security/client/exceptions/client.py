from core.exceptions import CustomException 
 
 
class ClientDuplicateException(CustomException): 
    code = 400 
    error_code = 10000 
    message = "duplicate client name" 
 
 
class ClientNotFoundException(CustomException): 
    code = 404 
    error_code = 10000 
    message = "client not found" 
