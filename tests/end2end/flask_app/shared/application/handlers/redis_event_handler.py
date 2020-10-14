from petisco import INFO, event_from_redis_message
from petisco.application.petisco import Petisco


def redis_event_handler(message):
    event = event_from_redis_message(message).unwrap_or_return()
    logger = Petisco.get_instance()._logger
    logger.log(INFO, event)
