from meiga import Error


class GivenNameIsNotValidError(Error):
    def __init__(self, message):
        self.message = message
