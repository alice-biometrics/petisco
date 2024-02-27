from enum import Enum


class MiddlewareScope(Enum):
    ALL = "all"
    CONTROLLER = "controller"
    SUBSCRIBER = "subscriber"
