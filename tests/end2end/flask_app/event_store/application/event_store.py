from petisco import Event
from meiga import BoolResult, isSuccess


def event_store(event: Event) -> BoolResult:
    print("event_store")
    return isSuccess
