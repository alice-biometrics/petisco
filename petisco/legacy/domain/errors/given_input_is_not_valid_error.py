from meiga import Error


class GivenInputIsNotValidError(Error):
    def __init__(self, message):
        self.message = message
