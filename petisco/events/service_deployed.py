from petisco.events.event import Event

EVENT_SERVICE_DEPLOYED_VERSION = 2


class ServiceDeployed(Event):
    app_name: str = None
    app_version: str = None

    def __init__(
        self,
        app_name: str,
        app_version: str,
        event_version: int = EVENT_SERVICE_DEPLOYED_VERSION,
    ):
        self.app_name = app_name
        self.app_version = app_version
        self.event_version = event_version

        super().__init__()
