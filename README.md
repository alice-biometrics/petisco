petisco
=======

Petisco is a framework for helping Python developers to build clean Applications

#### Installation 

```console
pip install petisco
```

###### Extras 

```console
pip install petisco[flask]
pip install petisco[sqlalchemy]
pip install petisco[redis]
pip install petisco[rabbitmq]
```

#### Getting Started

**petisco** provides us some sort of interfaces and decorators to help on the development of clean architecture Applications.

## Developers

##### Install requirements

```console
pip install -r requirements/dev.txt
```

##### Test

```console
pip install -e . && pytest
```

or if you are using flask extensions

```console
pip install -e .[flask] && pytest
```

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

##### Upload to PyPi 

```console
python setup.py sdist bdist_wheel
twine check dist/*
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```
