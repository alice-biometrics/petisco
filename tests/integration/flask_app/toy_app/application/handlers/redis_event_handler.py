from petisco import INFO, event_from_redis_message
from petisco.application.application_config import ApplicationConfig


def redis_event_handler(message):
    event = event_from_redis_message(message).unwrap_or_return()
    logger = ApplicationConfig.get_instance().logger
    logger.log(INFO, event)
