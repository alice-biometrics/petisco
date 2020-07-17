from meiga import Error


class SlackError(Error):
    def __init__(self, message):
        self.message = message
