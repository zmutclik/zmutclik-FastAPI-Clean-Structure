from core.exceptions import NotFoundException
 
class MenuNotFoundException(NotFoundException): 
    message = "menu not found" 
