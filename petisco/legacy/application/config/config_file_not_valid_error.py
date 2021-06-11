from meiga import Error


class ConfigFileNotValidError(Error):
    def __init__(self, message):
        self.message = message
