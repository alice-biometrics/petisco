# petisco :cookie:  [![version](https://img.shields.io/github/release/alice-biometrics/petisco/all.svg)](https://github.com/alice-biometrics/petisco/releases) [![ci](https://github.com/alice-biometrics/petisco/workflows/ci/badge.svg)](https://github.com/alice-biometrics/petisco/actions) [![pypi](https://img.shields.io/pypi/dm/petisco)](https://pypi.org/project/petisco/)

<img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/alice_header.png" width=auto>

Petisco is a framework for helping Python developers to build clean Applications in Python.

:warning: disclaimer: not stable yet


## Table of Contents
- [Installation :computer:](#installation-computer)
- [Getting Started :chart_with_upwards_trend:](#getting-started-chart_with_upwards_trend)
    * [Handlers](#handlers)
- [Extras](#extras)
- [Contact :mailbox_with_mail:](#contact-mailbox_with_mail)


## Installation :computer:

```console
pip install petisco
```

Installation with Extras 

```console
pip install petisco[flask]
pip install petisco[sqlalchemy]
pip install petisco[redis]
pip install petisco[rabbitmq]
pip install petisco[flask,sqlalchemy,redis,rabbitmq]
```

## Getting Started :chart_with_upwards_trend:	

**petisco** provides us some sort of interfaces and decorators to help on the development of clean architecture Applications.

### ApplicationConfig

Before to run your app, you should configure it with `ApplicationConfig` object.

`ApplicationConfig` is a singleton with the following parameters:

    Parameters
    ----------
    app_name
        Application name
    mode
        DeploymentMode define the toy_app mode of execution. If you're mapping services and repositories, please
        check given mode is mapped in services_mode_mapper and repositories_mode_mapper
    logger
        Pre configured logger
    config_dependencies
        Callable function to configure dependencies (e.g configure credentials in order to connect with a thrid-party
        toy_app.
    config_persistence
        Callable function to configure toy_app persistence (e.g configure a database)
    services_mode_mapper
        A dictionary to map DeploymentMode with a service provider function. This is used as a dependency injector
    repositories_mode_mapper
        A dictionary to map DeploymentMode with a repository provider function. This is used as a dependency injector
    event_manager
        A IEventManager valid implementation
    options
        A dictionary with specific toy_app options


Check a configuration example in the [Integration Tests](tests/integration/toy_app/application_setup.py)


### Handlers

**petisco** implement a sort of decorator to handle common behaviour of application elements.

#### Controller Handler

Add it to your entry point controller and manage the behaviour:

```python
    from petisco import controller_handler
    from meiga import Success

    @controller_handler()
    def my_controller(headers=None):
        return Success("Hello Petisco")
```
*controller_handler parameters:*

    Parameters
    ----------
    app_name
        Application name
    logger
        A ILogger implementation. Default NotImplementedLogger
    event_config
        EventConfig object. Here, you can define event management.
    jwt_config
        JwtConfig object. Here, you can define how to deal with JWT Tokens
    success_handler
        Handler to deal with Success Results
    error_handler
        Handler to deal with Failure Results
    correlation_id_provider
        Injectable function to provide correlation_id. By default is used flask_correlation_id_provider
    headers_provider
        Injectable function to provide headers. By default is used headers_provider
    logging_types_blacklist
        Logging Blacklist. Object of defined Type will not be logged. By default ( [bytes] ) bytes object won't be logged.


#### Extras

###### RabbitMQ

To test RabbitEventManager you need to run locally a RabbitMQ application, otherwise related test will be skipped.
Please, check the official doc here: https://www.rabbitmq.com/download.html

With docker

```console
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

How to use the RabbitMQEventManager:

```python
from time import sleep

from pika import ConnectionParameters
from petisco import Event, RabbitMQEventManager, UserId


class UserCreated(Event):
    user_id: UserId

    def __init__(self, user_id: UserId):
        self.user_id = user_id
        super().__init__()


def callback(ch, method, properties, body):
    event = Event.from_json(body)
    print(f" [x] Received {event}")
    # do your stuff here
    ok = True
    if ok:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_nack(delivery_tag=method.delivery_tag)


topic = "petisco"
event_manager = RabbitMQEventManager(
    connection_parameters=ConnectionParameters(host="localhost"),
    subscribers={topic: callback},
)

event_manager.send(
    topic, UserCreated(user_id=UserId.generate())
)

sleep(0.5)  # wait for the callback

event_manager.unsubscribe_all()
```

## Development

### Using lume

```console
pip install lume
```

Then:

```console 
lume -install -all
```


## Contact :mailbox_with_mail:

support@alicebiometrics.com
