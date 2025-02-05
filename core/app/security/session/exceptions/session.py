from core.exceptions import NotFoundException
 
class SessionNotFoundException(NotFoundException): 
    message = "session not registered" 
