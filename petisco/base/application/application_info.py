from datetime import datetime
from typing import Any, List, cast

from petisco.base.application.controller.error_map import ErrorMap
from petisco.base.application.middleware.middleware import Middleware
from petisco.base.misc.singleton import Singleton


class ApplicationInfo(metaclass=Singleton):
    name: str
    organization: str
    version: str
    deployed_at: datetime
    shared_error_map: ErrorMap
    shared_middlewares: List[Middleware]

    def __init__(self, **kwargs: Any) -> None:
        self.name = str(kwargs.get("name"))
        self.organization = str(kwargs.get("organization"))
        self.version = str(kwargs.get("version"))
        self.deployed_at = cast(datetime, kwargs.get("deployed_at"))
        self.shared_error_map = cast(dict, kwargs.get("shared_error_map", {}))
        self.shared_middlewares = cast(list, kwargs.get("shared_middlewares", []))
