from meiga import Error


class UnknownError(Error):
    def __init__(self, exception: Exception):
        self.message = f"{exception.__class__.__name__}: {str(exception)}"
