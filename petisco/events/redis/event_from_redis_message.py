from meiga import Result, Error, Success, isFailure

from petisco.events.event import Event


class EventFromRedisMessageConversionError(Error):
    pass


def event_from_redis_message(message) -> Result[Event, Error]:
    try:
        json_data = message["data"].decode("utf-8")
        event = Event.from_json(json_data)
        return Success(event)
    except:  # noqa E722
        return isFailure(EventFromRedisMessageConversionError())
