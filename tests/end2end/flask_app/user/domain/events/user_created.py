from petisco import Event


class UserCreated(Event):
    name: str

    def __init__(self, name: str, version: int = 1):
        self.name = name
        self.event_version = version
        super().__init__()
