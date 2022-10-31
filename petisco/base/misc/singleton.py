# class SingletonMeta(type):
#     """
#     The Singleton class can be implemented in different ways in Python. Some
#     possible methods include: base class, decorator, metaclass. We will use the
#     metaclass because it is best suited for this purpose.
#     """
#
#     _instances = {}
#
#     def __call__(cls, *args: Any, **kwargs: Any):
#         """
#         Possible changes to the value of the `__init__` argument do not affect
#         the returned instance.
#         """
#         if cls not in cls._instances:
#             instance = super().__call__(*args: Any, **kwargs: Any)
#             cls._instances[cls] = instance
#         return cls._instances[cls]
#
#
# class Singleton(metaclass=SingletonMeta):
#     pass
from typing import Any, Dict


class Singleton(type):
    _instances: Dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def clear(cls) -> None:
        try:
            del Singleton._instances[cls]
        except KeyError:
            pass
