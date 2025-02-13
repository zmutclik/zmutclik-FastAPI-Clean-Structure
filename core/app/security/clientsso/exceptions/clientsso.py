from core.exceptions import DuplicateValueException, NotFoundException


class ClientSSODuplicateException(DuplicateValueException):
    message = "duplicate clientsso id"


class ClientSSONotFoundException(NotFoundException):
    message = "client sso not found"
