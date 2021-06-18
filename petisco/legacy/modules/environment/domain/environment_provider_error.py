from meiga import Error


class EnvironmentProviderError(Error):
    def __init__(self, message):
        self.message = message
