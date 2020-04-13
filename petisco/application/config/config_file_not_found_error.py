from meiga import Error


class ConfigFileNotFoundError(Error):
    def __init__(self, filename):
        self.message = f"Petisco config file does not exist ({filename})"
