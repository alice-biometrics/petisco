Here, you will find comprehensive information and guidelines on migrating to a new version (v2) of petisco framework. 
Upgrading to the latest version can bring numerous benefits, including enhanced features, improved performance, and 
increased security. However, we understand that the migration process can be complex and challenging, which is why we 
have compiled this documentation to assist you every step of the way.


## Breaking Changes

Following changes may require modifications to your existing code. While we apologize for any inconvenience, we believe 
these updates will enhance functionality and improve user experience. Please review the accompanying documentation for 
specific modifications and reach out to our support team for assistance. We value your feedback and appreciate your 
understanding during this transition. Thank you for your continued support as we strive to provide you with an improved 
library experience.

### Dependencies 


!!! warning

    On dependency definition, `name` and `default_builder` are no longer available. 


=== "Petisco v1 👴"

    ````python hl_lines="4 8"
    from petisco import Container, Dependency
    
    dependencies = [
        Dependency(name="my-base", default_builder=Builder(MyImplementation))
    ]    
    Container.set_dependencies(dependencies)

    instance = Container.get("my-base")
    ````

=== "Petisco v2 👶"

    ````python hl_lines="4 8"
    from petisco import Container, Dependency
    
    dependencies = [
        Dependency(MyBase, builders={"default": Builder(MyImplementation)})
    ]    
    Container.set_dependencies(dependencies)

    instance = Container.get(MyBase)
    ````

For more info about new way of defining dependencies, you can check the [Dependency Injection Container section](../../application/#dependency-injection-container).

### Controller Result

!!! warning

    After some attempts to remove the forbidden petisco magic behind the controller returning type while keeping the useful
    mapping of the result (e.g. mapping Result values to outputs or Http errors in FastAPI) like in the [Issue 333](https://github.com/alice-biometrics/petisco/issues/333)
    , a new proposal have been validated.

    The main idea is simplify controller result to avoid the following question: **Is petisco controller going to return 
    me a `meiga.Result` or instead is going to directly map the Result using the Controller Config parameters (See [Doc](../../application/#configuration)).?**

    Now, the `Controller` implementation of petisco v2 version always returns a `meiga.Result` type. And this Result 
    type will have set a tranformed function to map domain result to the framework expected result (e.g. agging mapping 
    Result values to outputs or Http errors in FastAPI).


=== "Petisco v1 👴"

    ````python hl_lines="16"
    from petisco import DomainError, Controller, PrintMiddleware
    from meiga import Result, Success, Error
    import random
    
    class MyError(DomainError): ...
    
    class MyController(Controller):
        class Config:  
            success_handler = lambda result: {"message": "ok"}
            error_map = {NotFound: HttpError(status_code=404, detail="Task not Found")}
            middlewares = [PrintMiddleware]
    
        def execute(self) -> Result[bool, Error]:
            return Success(random.choice([True, False]))

    result = MyController().execute()
    ````

=== "Petisco v2 👶"

    ````python hl_lines="16 17 18 19 20"
    from petisco import DomainError, Controller, PrintMiddleware
    from meiga import Result, Success, Error
    import random
    
    class MyError(DomainError): ...
    
    class MyController(Controller):
        class Config: # 
            success_handler = lambda result: {"message": "ok"}
            error_map = {NotFound: HttpError(status_code=404, detail="Task not Found")}
            middlewares = [PrintMiddleware]
    
        def execute(self) -> Result[bool, Error]:
            return Success(random.choice([True, False]))

    result = MyController().execute()
    
    # If you want to transform you can do it with result.transform() o with a better semantic funciton `as_fastapi`
    from petisco.extras.fastapi import as_fastapi
    mapped_result = as_fastapi(result)
    ````

To use this in a FastAPI router, is quite easy:

=== "Petisco v1 👴"

    ````python
    from fastapi import APIRouter
    
    router = APIRouter()
    @router.get("my/path"):
    def my_router():
        result = MyController().execute() # real result don't match with typehint as it is mapped
        return result
    ````

=== "Petisco v2 👶"

    ```python hl_lines="2 8"
    from fastapi import APIRouter
    from petisco.extra.fastapi import as_fastapi

    router = APIRouter()
    @router.get("my/path"):
    def my_router():
        result = MyController().execute()
        return as_fastapi(result)
    ```

### MessageBuses 

!!! warning

    `DomainEventBus` and `CommandBus` do not implement `publish_list` anymore. Now is necessary to rename it to `publish`.
    The new `publish` implementation available in petisco v2 allows to pass individual and list of messages.

=== "Petisco v1 👴"

    ````python hl_lines="7"
    from petisco import Container, Dependency
    
    domain_events = [UserCreated(), UserCompleted()]

    domain_event_bus: DomainEventBus = MyDomainEventBus()  

    domain_event_bus.publish_list(domain_events)
    ````

=== "Petisco v2 👶"

    ```python hl_lines="7"
    from petisco import Container, Dependency
    
    domain_events = [UserCreated(), UserCompleted()]

    domain_event_bus: DomainEventBus = MyDomainEventBus()  

    domain_event_bus.publish(domain_events)
    ```


### Message Private Properties

!!! warning

    Petisco Message classes (`DomainEvent` and `Commnad`) had some limitations on version 1. Some `protected` class 
    attribute names cannot be chosen as were used to store meta information of the message.
    
    For example, you cannot use `name` attribute in your definition, or `version`.

    === "Petisco v1 👴"

    ````python hl_lines="4 5"
    from petisco import DomainEvent
    
    class UserCreated(DomainEvent):
        name: str 
        version: int
    ````

    Version 2 resolves this issues but needs to break compatibility.

Now, the access to private attributes must be performed using a sort of getters.

=== "Petisco v1 👴"

    ````python hl_lines="4 5 10 11"
    from petisco import DomainEvent
    
    class UserCreated(DomainEvent):
        name: str 
        version: int
        
        
    user_created = UserCreated(name"Alice", version=2)
    
    print(user_created.name) # the given name conflicts with private name attribute
    print(user_created.version) # the given version conflicts with private version attribute
    print(user_created.attributes) 
    print(user_created.message_id) 
    print(user_created.ocurred_on) 
    print(user_created.meta) 
    ````

=== "Petisco v2 👶"

    ```python 
    from petisco import DomainEvent
    
    class UserCreated(DomainEvent):
        name: str 
        version: int
        
        
    user_created = UserCreated(name"Alice", version=2)
    
    print(user_created.get_message_name()) 
    print(user_created.get_message_version()) 
    print(user_created.get_message_attributes()) 
    print(user_created.get_message_id()) 
    print(user_created.get_message_ocurred_on()) 
    print(user_created.get_message_meta()) 
    ```

### Message (From metaclass to Pydantic)

!!! warning

    Petisco `Message` base class is now a `pydantic.BaseModel`. This will help on dev experience improvement of 
    `DomainEvent` and `Command` and also validation. [https://github.com/alice-biometrics/petisco/issues/360](https://github.com/alice-biometrics/petisco/issues/360)



To ilustrate main changes we will use the following `DomainEvent` definition:

```python
from petisco import DomainEvent

class UserCreated(DomainEvent):
    name: str
    age: int

user_created = UserCreated(name="acme", age=50)
```

Main changes:

* Serialization
  * Use `.format()` instead of `.dict()` to convert your Message to specific message format.
    ```python
    {'data': {'id': '01d34093-7b7f-43b0-8cdf-557bb377c331', 'type': 'user.created', 'type_message': 'domain_event', 'version': 1, 'occurred_on': '2023-07-17 15:35:03.518701', 'attributes': {'name': 'acme', 'age': 50}, 'meta': {}}}
    ```
  * Use `.format_json()` instead of `.json()` to convert your Message to specific message format and convert to str.
    ```python
    "{'data': {'id': '01d34093-7b7f-43b0-8cdf-557bb377c331', 'type': 'user.created', 'type_message': 'domain_event', 'version': 1, 'occurred_on': '2023-07-17 15:35:03.518701', 'attributes': {'name': 'acme', 'age': 50}, 'meta': {}}}"
    ```
  * Use `.model_dump()` (old pydantic `.dict()`) to get model attributes dictionary:
    ```python
    {'name': 'acme', 'age': 50}
    ```
  * Use `.model_dump_json()` (old pydantic `.json()`) to get model attributes dictionary:
    ```python
    "{'name': 'acme', 'age': 50}"
    ```
* Deserialization
  * Use `.from_format(formatted_message: dict | str | bytes)` to convert from specific message format (`.format()` and `.format_json()` output). Don't use legacy `.from_dict()`.
* New features thanks to pydantic
  * Attribute auto-completion
  * Atrribute and model validation as we are extending from `pydantic.BaseModel`
  * Automatic serialization 

If something is wrong with new `Message` class your can change to previous implementation via envar:

```bash
export PETISCO_MESSAGE_AS_PYDANTIC_MODEL=disable
```

## Dev Experience Improvements

### Retrieved Message are better typed


!!! info

    In the [Issue 340](https://github.com/alice-biometrics/petisco/issues/340) is implemented an improvement to access 
    attributes of retrieved Messages (DomainEvent and Commands).

=== "Petisco v1 👴"

    ````python hl_lines="15"
    from typing import Type
    from meiga import isSuccess
    from petisco import DomainEventSubscriber, DomainEvent, Container

    class TaskCreated(DomainEvent):
        name: str
    
    class SendNotificationOnTaskModifications(DomainEventSubscriber):
    
        def subscribed_to(self) -> list[Type[DomainEvent]]:
            return [TaskCreated] 
    
        def handle(self, domain_event: DomainEvent) -> BoolResult:

            task_name = domain_event.attributes.get("name")
            
            # Do your stuff here

            return isSuccess
    ````

=== "Petisco v2 👶"

    ````python hl_lines="15"
    from typing import Type
    from meiga import isSuccess
    from petisco import DomainEventSubscriber, DomainEvent, Container

    class TaskCreated(DomainEvent):
        name: str
    
    class SendNotificationOnTaskModifications(DomainEventSubscriber):
    
        def subscribed_to(self) -> list[Type[DomainEvent]]:
            return [TaskCreated] 
    
        def handle(self, domain_event: TaskCreated) -> BoolResult:

            task_name = domain_event.name # With typehint and autocompletion.
            
            # Do your stuff here

            return isSuccess
    ````

### Async Implementations 

!!! info

    Petisco v2 provides async implementation for every base elements. This allows petisco users to migrate step their 
    use cases, controllers and app services keeping back compatibility with current sync implementations.


=== "Petisco v1 👴 (sync)"

    ```python hl_lines="10 16"
    from meiga import BoolResult
    from petisco import Container, DomainEventBus
    from petisco.extra.fastapi import FastAPIController
    
    from app.src.task.create.application.task_creator import TaskCreator
    from app.src.task.shared.domain.task import Task
    
    
    class CreateTaskController(FastAPIController):
        def execute(self, task: Task) -> BoolResult:
            task_creator = TaskCreator(
                labeler=Container.get(TaskLabeler),
                repository=Container.get(TaskRepository),
                domain_event_bus=Container.get(DomainEventBus),
            )
            return task_creator.execute(task=task)
    ```

=== "Petisco v2 👶 (sync -> no changes)"

    ```python hl_lines="10 16"
    from meiga import BoolResult
    from petisco import Container, DomainEventBus
    from petisco.extra.fastapi import FastAPIController
    
    from app.src.task.create.application.task_creator import TaskCreator
    from app.src.task.shared.domain.task import Task
    
    
    class CreateTaskController(FastAPIController):
        def execute(self, task: Task) -> BoolResult:
            task_creator = TaskCreator(
                labeler=Container.get(TaskLabeler),
                repository=Container.get(TaskRepository),
                domain_event_bus=Container.get(DomainEventBus),
            )
            return task_creator.execute(task=task)
    ```

=== "Petisco v2 👶 (async ⚡)"

    ```python hl_lines="9 10 16"
    from meiga import BoolResult
    from petisco import Container, DomainEventBus
    from petisco.extra.fastapi import AsyncFastAPIController
    
    from app.src.task.create.application.task_creator import AsyncTaskCreator
    from app.src.task.shared.domain.task import Task
    
    
    class CreateTaskController(AsyncFastAPIController):
        async def execute(self, task: Task) -> BoolResult:
            task_creator = AsyncTaskCreator(
                labeler=Container.get(TaskLabeler),
                repository=Container.get(TaskRepository),
                domain_event_bus=Container.get(DomainEventBus),
            )
            return await task_creator.execute(task=task)
    ```

### Use `shared_error_map`

!!! info

    Petisco v2 provides an implementation for configure shared error maps

Check `error_map` documentation in [Application/Configuration](../../application/#configuration) to know hot to ease 
your error handling.