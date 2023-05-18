Here, you will find comprehensive information and guidelines on migrating to a new version (v2) of petisco framework. 
Upgrading to the latest version can bring numerous benefits, including enhanced features, improved performance, and 
increased security. However, we understand that the migration process can be complex and challenging, which is why we 
have compiled this documentation to assist you every step of the way.


## Breaking Changes

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
    from petisco.extra.fastapi import AsyncFastAPIController
    
    from app.src.task.create.application.task_creator import TaskCreator
    from app.src.task.shared.domain.task import Task
    
    
    class CreateTaskController(AsyncFastAPIController):
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
    from petisco.extra.fastapi import AsyncFastAPIController
    
    from app.src.task.create.application.task_creator import TaskCreator
    from app.src.task.shared.domain.task import Task
    
    
    class CreateTaskController(AsyncFastAPIController):
        def execute(self, task: Task) -> BoolResult:
            task_creator = TaskCreator(
                labeler=Container.get(TaskLabeler),
                repository=Container.get(TaskRepository),
                domain_event_bus=Container.get(DomainEventBus),
            )
            return task_creator.execute(task=task)
    ```

=== "Petisco v2 👶 (async ⚡)"

    ```python hl_lines="10 16"
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