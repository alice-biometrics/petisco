from petisco.extra.rabbitmq.is_pika_available import is_pika_available

rabbitmq = []
if is_pika_available():
    from petisco.extra.rabbitmq.dependencies import (
        get_extra_bus_dependencies as get_available_bus_dependencies,
    )

    rabbitmq = ["get_available_bus_dependencies"]
else:
    from petisco.extra.rabbitmq.dependencies import (
        get_basic_bus_dependencies as get_available_bus_dependencies,
    )

    rabbitmq = ["get_available_bus_dependencies"]

__all__ = rabbitmq
