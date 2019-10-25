from petisco.logger.logger import Logger


class FakeLogger(Logger):
    def __init__(self):
        self.logging_messages = []

    def log(self, logging_level, message):
        self.logging_messages.append((logging_level, message))

    def get_logging_messages(self):
        return self.logging_messages
