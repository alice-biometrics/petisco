# petisco 🍪  [![version](https://img.shields.io/github/release/alice-biometrics/petisco/all.svg)](https://github.com/alice-biometrics/petisco/releases) [![ci](https://github.com/alice-biometrics/petisco/workflows/ci/badge.svg)](https://github.com/alice-biometrics/petisco/actions) [![pypi](https://img.shields.io/pypi/dm/petisco)](https://pypi.org/project/petisco/)

<img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/alice_header.png" width=auto>

Petisco is a framework for helping Python developers to build clean Applications in Python.

⚠️ Disclaimer: Current version now is v1 (not stable yet). 
Find deprecated version (v0) in `legacy` branch.


## Installation :computer:

```console
pip install petisco
```

Installation with Extras 

```console
pip install petisco[fastapi,sqlalchemy,elastic,rabbitmq,slack,redis]
```

## Getting Started :chart_with_upwards_trend:	
    
### Model your Domain

`petisco 🍪` is a framework which helps you to model you domain. 
Imagine you have a domain where your business logic is to manage a task system, let's see some examples that can help you.

#### UUID

Use `Uuid` to generate new identifiers.

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

Use `DomainEvent` to explicitly implement side effects of changes within your domain.

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

`DomainEvent` inherits from `Message` that have available `dict` and `json` method to encode the info.

```python
my_domain_event = TaskCreated(task_id=TaskId.v4())

print(my_domain_event.json())
```

The result should be something like the following:
```json
{"data": {"id": "3a4d78aa-6870-41cb-aa14-964831511d86", "type": "task.created", "type_message": "domain_event", "version": 1, "occurred_on": "2021-12-28 14:11:47.845618", "attributes": {"task_id": "a7f8b62a-c9e5-4f3c-a451-47cd1965958f"}, "meta": {}}}
```

If you use CQRS you can use also the `Command` class.

```python
from petisco import Command, Uuid

class TaskId(Uuid):
    pass

class UpdateTask(Command):
    task_id: TaskId

my_command = UpdateTask(task_id=TaskId.v4())

print(my_command.json())
```

The result:

```json
{"data": {"id": "1f35e414-0636-4983-987e-13d522749709", "type": "update.task", "type_message": "command", "version": 1, "occurred_on": "2021-12-28 14:19:09.149651", "attributes": {"task_id": "db0970be-f6b6-478b-976a-f83e85112b90"}, "meta": {}}}
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

To test how petisco can help you on rabbitmq queues management you need to run locally a RabbitMQ application, otherwise related test will be skipped.
Please, check the official doc here: https://www.rabbitmq.com/download.html.

Run RabbitMQ with docker

```console
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

You can check the RabbitMQ status on [http://localhost:15672/#/](http://localhost:15672/#/) (guest:guest).

Find [here](examples/rabbitmq) some petisco examples.

**Configure the rabbitmq**

```console
python examples/rabbitmq/configure.py
```

**Start consuming messages**

```console
python examples/rabbitmq/consume.py
```

**Publish some Domain Events**

```console
python examples/rabbitmq/publish_domain_events.py
```

**Dispatch a Command**

```console
python examples/rabbitmq/dispatch_commands.py
```

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
