from petisco.events.event import Event


class ServiceDeployed(Event):
    app_name: str = None
    app_version: str = None

    def __init__(self, app_name: str, app_version: str):
        self.app_name = app_name
        self.app_version = app_version
        super().__init__()
