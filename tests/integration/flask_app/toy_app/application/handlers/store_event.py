from petisco import Event
from petisco.events.subscriber.domain.subscriber_handler import subscriber_handler


@subscriber_handler()
def store_event(event: Event):
    print(f"Event: {event}")
