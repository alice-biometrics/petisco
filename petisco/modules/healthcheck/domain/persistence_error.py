from meiga import Error


class PersistenceError(Error):
    def __init__(self, message):
        self.message = message
