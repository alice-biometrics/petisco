__all__ = []

from petisco.extra.rabbitmq.is_pika_available import is_pika_available

if is_pika_available():
    from petisco.extra.rabbitmq.shared.dependencies import get_bus_dependencies

    __all__ = ["get_bus_dependencies"]
