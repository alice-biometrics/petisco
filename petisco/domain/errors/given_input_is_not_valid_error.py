from meiga import Error


class GivenInputIsNotValidError(Error):
    def __init__(self, message):
        self.message = f"{self.__class__.__name__:s}: [{message:s}]"
