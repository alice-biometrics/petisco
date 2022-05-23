# petisco 🍪  [![version](https://img.shields.io/github/release/alice-biometrics/petisco/all.svg)](https://github.com/alice-biometrics/petisco/releases) [![ci](https://github.com/alice-biometrics/petisco/workflows/ci/badge.svg)](https://github.com/alice-biometrics/petisco/actions) [![pypi](https://img.shields.io/pypi/dm/petisco)](https://pypi.org/project/petisco/) [![codecov](https://codecov.io/gh/alice-biometrics/petisco/branch/main/graph/badge.svg?token=YHXAYKX0VO)](https://codecov.io/gh/alice-biometrics/petisco)



<img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/alice_header.png?raw=true" width=auto>

Petisco is a framework for helping Python developers to build clean Applications in Python.

⚠️ Disclaimer: Current version now is v1 (not stable yet). 
Find deprecated version (v0) in `legacy` branch.


## Installation 💻

```console
pip install petisco
```

Installation with Extras 

```console
pip install petisco[fastapi,sqlalchemy,elastic,rabbitmq,slack,redis]
```

## Getting Started 📈
    
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

class TaskId(Uuid): ...

task_id = TaskId.v4()
```

#### Domain Event

Use `DomainEvent` to explicitly implement side effects of changes within your domain.

```python
from petisco import DomainEvent, Uuid

class TaskId(Uuid): ...

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

class TaskId(Uuid): ...

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

class TaskAlreadyExistError(DomainError): ...
class TaskNotFoundError(DomainError): ...
```

You can add additional information to `DomainError` objects with:

```python
domain_error = TaskNotFoundError(additional_info={"error": "detail"})
```

or also you can add releated uuid with 

```python
domain_error = TaskNotFoundError(uuid_value=task_id.value, additional_info={"error": "detail"})
```

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

#### Controller

Use `Controller` class to define and configure inputs and outputs or your entry point.

You can use a simpler and default configuration
```python
from petisco Controller
import random

class MyController(Controller):
    def execute(self) -> bool:
        return random.choice([True, False])
```

Or define some configurations using the inner class `Config`


```python
from petisco DomainError, Controller, PrintMiddleware
import random

class MyError(DomainError): ...

class MyController(Controller):
    class Config:
        middlewares = [PrintMiddleware]
        success_handler = lambda result: {"message": f"MyController set {result}"} 
        error_map = {MyError: {"message": "something wrong happens"}}

    def execute(self) -> bool:
        return random.choice([True, False])
```

If you want to set a default middleware for every Controller, you can use the envvar `PETISCO_DEFAULT_MIDDLEWARES`:
  * `PETISCO_DEFAULT_MIDDLEWARES=PrintMiddleware`: to configure PrintMiddleware
  * `PETISCO_DEFAULT_MIDDLEWARES=NotifierMiddleware`: to configure NotifierMiddleware
  * `PETISCO_DEFAULT_MIDDLEWARES=PrintMiddleware,NotifierMiddleware`: to configure several middlewares
  

#### Message Broker 

petisco 🍪 provides several classes to help on the construction of Message publishers and consumers using a message broker.

Please, find more information in [doc/message_broker/MessageBroker.md](doc/message_broker/MessageBroker.md).

## Development

### Using lume

```console
pip install lume
```

Then:

```console 
lume -install -all
```


## Contact 📬

support@alicebiometrics.com
