from meiga import Error


class EmptyValueObjectError(Error):
    def __init__(self, message):
        self.message = message
