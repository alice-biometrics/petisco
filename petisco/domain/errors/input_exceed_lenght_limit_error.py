from meiga import Error


class InputExceedLengthLimitError(Error):
    def __init__(self, message):
        self.message = message
