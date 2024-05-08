import contextlib
from typing import Any, Dict


class Singleton(type):
    _instances: Dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        force = kwargs.get("force_recreation", False)

        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        elif force:
            cls.clear()
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def clear(cls) -> None:
        with contextlib.suppress(KeyError):
            del Singleton._instances[cls]
