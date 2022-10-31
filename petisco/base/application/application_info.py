from datetime import datetime
from typing import Any, cast

from petisco.base.misc.singleton import Singleton


class ApplicationInfo(metaclass=Singleton):
    name: str
    organization: str
    version: str
    deployed_at: datetime

    def __init__(self, **kwargs: Any) -> None:
        self.name = str(kwargs.get("name"))
        self.organization = str(kwargs.get("organization"))
        self.version = str(kwargs.get("version"))
        self.deployed_at = cast(datetime, kwargs.get("deployed_at"))
