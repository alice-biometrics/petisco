Petisco has several classes available to help you take advantage of the asyncio library. For example, the 
AsyncController class provides a way to handle requests asynchronously, while the AsyncUseCase class offers an async 
interface for implementing your business logic. These classes can be used to write highly performant and efficient code 
that takes full advantage of the capabilities of the asyncio library.


### `AsyncAppService`

### `AsyncUseCase`

### `AsyncController`

```python hl_lines="5"
from petisco import AsyncController
from meiga import Result, Success, Error
import random

class MyController(AsyncController): # (1)
    async def execute(self) -> Result[bool, Error]:
        return Success(random.choice([True, False]))
```

1. Inherit from petisco AsyncController class

#### FastAPI ⚡️

Use `AsyncFastAPIController` instead of using `FastAPIController`.

```python hl_lines="9 10 11 12 13 14 15 16"
from meiga import BoolResult
from petisco import Container, DomainEventBus
from petisco.extra.fastapi import AsyncFastAPIController

from app.src.task.create.application.task_creator import TaskCreator
from app.src.task.shared.domain.task import Task


class CreateTaskController(AsyncFastAPIController):
    async def execute(self, task: Task) -> BoolResult:
        task_creator = TaskCreator(
            labeler=Container.get(TaskLabeler),
            repository=Container.get(TaskRepository),
            domain_event_bus=Container.get(DomainEventBus),
        )
        return await task_creator.execute(task=task)
```

Then, we have to instantiate and execute the controller object in the FastAPI routers.

```python hl_lines="11 12 13"
from uuid import UUID

from fastapi import APIRouter
from petisco.extra.fastapi import as_fastapi
from petisco import Uuid

from app.api.models import TaskIn, TaskOut
from app.src.task.create.application.create_task_controller import CreateTaskController

router = APIRouter(tags=["Tasks"])

@router.post("/task")
async def create_task(task: TaskIn):
    result = await CreateTaskController().execute(task.to_task())
    return as_fastapi(result)
    
```
