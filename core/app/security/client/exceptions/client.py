from core.exceptions import NotFoundException
 
class ClientNotFoundException(NotFoundException): 
    message = "client not registered" 
