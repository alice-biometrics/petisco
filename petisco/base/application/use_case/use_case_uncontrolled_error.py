from meiga import Error


class UseCaseUncontrolledError(Error):
    def __init__(self, exception: Exception):
        self.exception = exception
