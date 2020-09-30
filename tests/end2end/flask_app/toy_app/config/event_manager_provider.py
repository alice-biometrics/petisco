from petisco import IEventManager, NotImplementedEventManager


def event_manager_provider() -> IEventManager:
    return NotImplementedEventManager()
