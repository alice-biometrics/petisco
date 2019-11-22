from petisco import INFO
from petisco.application.application_config import ApplicationConfig
from petisco.events.event import Event
from petisco.events.redis.redis_based_event_handler import redis_based_event_handler


@redis_based_event_handler
def user_created_handler(event: Event):
    logger = ApplicationConfig.get_instance().logger
    logger.log(INFO, event)
