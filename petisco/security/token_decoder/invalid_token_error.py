from meiga import Error


class InvalidTokenError(Error):
    def __init__(self, message: str = None):
        self.message = message
