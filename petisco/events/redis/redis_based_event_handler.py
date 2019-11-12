from petisco.events.event import Event


def redis_based_event_handler(func):
    def wrapper(message):
        json_data = message["data"].decode("utf-8")
        event = Event.from_json(json_data)
        return func(event)

    return wrapper
