This package helps on the creation of web applications. `petisco` provides several classes to help model the domain and 
manage the lifecycle of applications with a hexagonal architecture. In addition, it provides abstractions to extend with
your infrastructure details.

!!! note "Versions"
    First version of `petisco` (v0) born quite coupled to [Flask](https://flask.palletsprojects.com/en/2.2.x/) web framework.
    Now, `petisco` v1 is not coupled to any web framework. Nevertheless, the package provides some examples and useful tool to 
    speed up the integration with the awesome [FastAPI](https://fastapi.tiangolo.com/) framework.

Let's review what `petisco` offers starting with the application layer.

```mermaid
flowchart LR

		subgraph I/O
		cli([CLI])
        webapp([Web App])
        message([Message Broker])
		end
		
		subgraph Application
		controller([Controller])
		usecase([UseCase])
		subscriber([Subscriber])
		controller --> usecase
		subscriber --> usecase
		end
		
		webapp --> controller
		cli --> controller
		message --> subscriber

		subgraph Domain
        petisco(((petisco)))
		end
		
		usecase --> petisco

		subgraph Infrastructure
		Persistence[(Persistence)]
		petisco --> Persistence
		petisco --> Buses
		petisco --> Monitoring
		petisco --> Others
		end
		
		style Application fill:#D6EAF8
```

## Application

The following code is the minimum to define and configure an application:

```python
from petisco import Application
from datetime import datetime

application = Application(
    name="my-app",
    version="1.0.0",
    organization="acme",
    deployed_at=str(datetime.utcnow()),
    environment="staging",

)
application.configure()
```

Since no dependencies or configurators have been added, running `configure` will have no side effects.

### Define your Dependencies 🎯

```mermaid
flowchart LR
		subgraph Application
        configure([Configure])
		end
	
	    configure -- Set Dependencies --> Container
	
		style configure fill:#D6EAF8
```

You can define your dependencies adding a callable (dependencies_provider - `Optional[Callable[..., List[Dependency]]]`).

```python
from petisco import (
    Application,
    Dependency,
    Builder,
    InmemoryCrudRepository,
    AggregateRoot,
)
from datetime import datetime

class Task(AggregateRoot): ...

# Class to define your dependencies 🎯
def dependencies_provider() -> list[Dependency]:
    dependencies = [
        Dependency( 
            name="task_repository",
            default_builder=Builder(InmemoryCrudRepository[Task])
        )
    ]
    return dependencies


application = Application(
    name="my-app",
    version="1.0.0",
    organization="acme",
    deployed_at=str(datetime.utcnow()),
    environment="staging",
    dependencies_provider=dependencies_provider,  # <==== Adding dependencies ➕
)
application.configure()
```

When call `configure` method, dependencies will be checked and added to the `Container` of dependencies being ready to be consumed
to inject them to the use cases.

???+ tip

    Different implementations can be specified for each `Dependency`, depending on environment variables.
    
    ```python
    from petisco import (
        Dependency,
        Builder,
        InmemoryCrudRepository,
        AggregateRoot
    )
    from my_app import FolderTaskCrudRepository, MySQLTaskCrudRepository, ElasticTaskCrudRepository
    
    class Task(AggregateRoot): ...
    
    def dependencies_provider() -> list[Dependency]:
        dependencies = [
            Dependency( 
                name="task_repository",
                default_builder=Builder(InmemoryCrudRepository[Task]), # <== default implementation 
                envar_modifier="TASK_REPOSITORY_TYPE", # <== env variable acts as modificator
                builders={
                    "folder": Builder(
                        FolderTaskCrudRepository, folder="folder_task_database" # Here we have to add required parameter on the implementation constructor
                    ),
                    "mysql": Builder(
                        MySQLTaskCrudRepository, connection="whatever required" # Here we have to add required parameter on the implementation constructor
                    ),
                    "elastic": Builder(
                        ElasticTaskCrudRepository, connection="whatever required" # Here we have to add required parameter on the implementation constructor
                    )
                },
            )
        ]
        return dependencies
    ```

    When envar `TASK_REPOSITORY_TYPE` is not defined, default implementation is `InmemoryCrudRepository`.
    When `TASK_REPOSITORY_TYPE` has a valid value (available as a key in the `builders` dictation) the implementation 
    will be changed. These are the options configured in the `builders` dictionary :

    * `FolderTaskCrudRepository`
    * `MySQLTaskCrudRepository`
    * `ElasticTaskCrudRepository`

### Add Application Configurers 🛠️

```mermaid
flowchart LR
		subgraph Application
        configure([Configure])
		end
		
		appconfig1([Application Configurer 1])
		appconfig2([Application Configurer 2])
		appconfign([Application Configurer N])

	    configure -- Run --> appconfig1
	    configure -- Run --> appconfig2
	    configure -- Run --> appconfign

		style configure fill:#D6EAF8
```

Extend from `ApplicationConfigurer` to model logics we want to be executed at application startup.

```python
from petisco import (
    Application,
    ApplicationConfigurer,
    AggregateRoot,
    Container
)
from datetime import datetime

class Task(AggregateRoot): 
    name: str
    description: str

# Configurer to add tasks to a specific repository (e.g. to init a tutorial)
class AddTasksForTutorialApplicationConfigurer(ApplicationConfigurer):
    def __init__(self, tasks: list[Task]):
        self.tasks = tasks
        execute_after_dependencies = True
        super().__init__(execute_after_dependencies)

    def execute(self, testing: bool = False) -> None:
        repository = Container.get("task_repository")
        for task in self.tasks:
            repository.save(task)
        
configurers = [
    AddTasksForTutorialApplicationConfigurer(
        tasks=[Task(name="petisco", description="Learning petisco is nice!")]
    )
]

application = Application(
    name="my-app",
    version="1.0.0",
    organization="acme",
    deployed_at=str(datetime.utcnow()),
    environment="staging",
    configurers=configurers,  # <==== Adding your configurers ➕
)
application.configure()
```

???+ tip "Use `testing` parameter"

    You can define diferent behaivor for testing environment using `testing` both in `ApplicationConfigurers` and `Application.configure` method.

    ```python
    import os
    from petisco import (
        Application,
        ApplicationConfigurer,
        AggregateRoot,
        Container
    )
    from datetime import datetime
    
    class Task(AggregateRoot): 
        name: str
        description: str
    
    # Configurer to perform an action only in testing
    class OnlyTestingApplicationConfigurer(ApplicationConfigurer):
        def __init__(self):
            execute_after_dependencies = True
            super().__init__(execute_after_dependencies)
    
        def execute(self, testing: bool = False) -> None:
            if not testing:
                return
            
            notifier = Container.get("notifies")
            notifier.send_message("Message to Github Actions")
            
    configurers = [
        OnlyTestingApplicationConfigurer(
            tasks=[Task(name="petisco", description="Learning petisco is nice!")]
        )
    ]
    
    application = Application(
        name="my-app",
        version="1.0.0",
        organization="acme",
        deployed_at=str(datetime.utcnow()),
        environment="staging",
        configurers=configurers,  # <==== Adding your configurers ➕
    )

    testing = strtobool(os.getenv("TESTING", "false"))
    application.configure(testing)
    ```

### Other methods 👌

| Method                                             | Definition                                                                         | 
|----------------------------------------------------|:-----------------------------------------------------------------------------------| 
| `get_dependencies()`                               | Return a list of set dependencies                                                  | 
| `clear()`                                          | Clear set dependencies                                                             |  
| `info()`                                           | Returns a json with information of the application and its configured dependencies |
| `publish_domain_event(domain_event: DomainEvent)`  | Publish a domain event using configured `DomainEventBus` dependency                |  
| `notify(message: NotifierMessage)`                 | Notify a message using configured `Notifier` dependency                      |
| `was_deploy_few_minutes_ago(minutes: int = 25)`    | Useful to decide some notification depending on when was the application deployed  |

