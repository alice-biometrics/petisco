from petisco import LogMessage
from petisco.logger.interface_logger import ILogger


class FakeLogger(ILogger):
    def __init__(self):
        self.logging_messages = []

    def log(self, logging_level, log_message: LogMessage):
        self.logging_messages.append((logging_level, log_message.to_dict()))

    def get_logging_messages(self):
        return self.logging_messages
