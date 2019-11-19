from petisco.logger.interface_logger import ILogger


class FakeLogger(ILogger):
    def __init__(self):
        self.logging_messages = []

    def log(self, logging_level, message):
        self.logging_messages.append((logging_level, message))

    def get_logging_messages(self):
        return self.logging_messages
