# petisco 🍪  [![version](https://img.shields.io/github/release/alice-biometrics/petisco/all.svg)](https://github.com/alice-biometrics/petisco/releases) [![ci](https://github.com/alice-biometrics/petisco/workflows/ci/badge.svg)](https://github.com/alice-biometrics/petisco/actions) [![pypi](https://img.shields.io/pypi/dm/petisco)](https://pypi.org/project/petisco/)

<img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/alice_header.png" width=auto>

Petisco is a framework for helping Python developers to build clean Applications in Python.

⚠️ disclaimer: Current version now is v1 (not stable yet). 
You can found the deprecated version v0 in `v0` branch,


## Installation :computer:

```console
pip install petisco
```

Installation with Extras 

```console
pip install petisco[fastapi]
pip install petisco[sqlalchemy]
pip install petisco[redis]
pip install petisco[rabbitmq]
pip install petisco[fastapi,sqlalchemy,redis,rabbitmq]
```

## Getting Started :chart_with_upwards_trend:	
    
### Model your Domain

`petisco 🍪` is a framework which helps you to model you domain. 
Imagine you have a domain where your business logic is to manage a task system, let's see some examples that can help you.

#### UUID

Use `Uuid` to generate new identificators

```python
from petisco import Uuid
uuid = Uuid.v4()
```

Additionally, you can extend it:

```python
from petisco import Uuid

class TaskId(Uuid):
    pass

task_id = TaskId.v4()
```

#### Domain Event

```python
from petisco import DomainEvent, Uuid

class TaskId(Uuid):
    pass

class TaskCreated(DomainEvent):
    task_id: TaskId


class TaskRemoved(DomainEvent):
    task_id: TaskId

class TaskRetrieved(DomainEvent):
    task_id: TaskId
```


#### Domain Error

```python
from petisco import DomainError


class TaskAlreadyExistError(DomainError):
    pass


class TaskNotFoundError(DomainError):
    pass
```

⚠️ TODO: Add documentation on how to specify the message

#### Value Objects

Extend `ValueObject` to model your Value Objects.

```python
from pydantic import validator
from meiga import Failure
from petisco import ValueObject, DomainError

class EmptyValueObjectError(DomainError): pass
class ExceedLengthLimitValueObjectError(DomainError): pass

def ensure_not_empty_value(value, classname: str = None):
    if value is None:
        raise Failure(EmptyValueObjectError(classname))


def ensure_value_is_less_than_200_char(value):
    if len(value) > 200:
        raise ExceedLengthLimitValueObjectError(value)


class Description(ValueObject):

    @validator('value')
    def validate_value(cls, value):
        ensure_not_empty_value(value, cls.__name__)
        ensure_value_is_less_than_200_char(value)
        return value.title()
```

#### Aggregate Root

Extend `AggregateRoot` to model your Aggregate Roots
 
```python
from petisco import AggregateRoot
from datetime import datetime

from app.src import Description
from app.src.tasks.shared.domain.events import TaskCreated
from app.src.tasks.shared.domain.task_id import TaskId
from app.src.tasks.shared.domain.title import Title


class Task(AggregateRoot):
    title: Title
    description: Description
    created_at: datetime

    @staticmethod
    def create(task_id: TaskId, title: Title, description: Description):
        task = Task(aggregate_id=task_id, title=title, description=description, created_at=datetime.utcnow())
        task.record(TaskCreated(task_id=task_id))
        return task
```

⚠️ TODO: How we can take advantage of aggregate root (pull_domain_events, record)

#### Messages 
⚠️ TODO: How we use the Message Manager!

### Testing :white_check_mark:

#### Extras

###### RabbitMQ <img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/rabbitmq.png" width="16">

⚠️ TODO: It is outdated (v0)

To test RabbitEventManager you need to run locally a RabbitMQ application, otherwise related test will be skipped.
Please, check the official doc here: https://www.rabbitmq.com/download.html

Run RabbitMQ with docker

```console
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Please, check examples in [examples/pubsub](examples/pubsub)

Run a Subscriber

```console
python examples/pubsub/sub.py
```

Run a Publisher:

```console
python examples/pubsub/pub.py
```

Run a Subscriber linked to a dead letter queues.

```console
python examples/pubsub/dl_sub.py
```

This can be used to requeue nack events.


##### Configurations

* `RABBITMQ_HEARTBEAT`: (default: 60 s)
* `RABBITMQ_USER`: (default: guest)
* `RABBITMQ_PASSWORD`: (default: guest)
* `RABBITMQ_HOST`: (default: localhost)
* `RABBITMQ_HOST`: (default: 5672)
* `RABBITMQ_CONNECTION_NUM_MAX_RETRIES`: (default: 15)
* `RABBITMQ_CONNECTION_WAIT_SECONDS_RETRY`: (default: 1)
* `RABBITMQ_MESSAGE_TTL`: (default 1000 ms) If a queue is already created it will generate a precodition failure.


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
