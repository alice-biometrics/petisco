from petisco.logger.interface_logger import ILogger


class NotImplementedLogger(ILogger):
    def log(self, logging_level, message):
        pass
