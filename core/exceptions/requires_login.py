class RequiresLoginException(Exception):
    def __init__(self, nextRouter: str = "/page/login"):
        self.nextRouter = nextRouter
