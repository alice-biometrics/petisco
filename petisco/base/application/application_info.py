from datetime import datetime

from petisco.base.misc.singleton import Singleton


class ApplicationInfo(metaclass=Singleton):
    name: str
    organization: str
    version: str
    deployed_at: datetime

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.organization = kwargs.get("organization")
        self.version = kwargs.get("version")
        self.deployed_at = kwargs.get("deployed_at")
