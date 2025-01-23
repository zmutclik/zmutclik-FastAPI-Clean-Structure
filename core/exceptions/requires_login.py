class RequiresLoginException(Exception):
    def __init__(self, nextRouter: str = "/auth/login"):
        self.nextRouter = nextRouter
