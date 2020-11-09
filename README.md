# petisco :cookie:  [![version](https://img.shields.io/github/release/alice-biometrics/petisco/all.svg)](https://github.com/alice-biometrics/petisco/releases) [![ci](https://github.com/alice-biometrics/petisco/workflows/ci/badge.svg)](https://github.com/alice-biometrics/petisco/actions) [![pypi](https://img.shields.io/pypi/dm/petisco)](https://pypi.org/project/petisco/)

<img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/alice_header.png" width=auto>

Petisco is a framework for helping Python developers to build clean Applications in Python.

:warning: disclaimer: not stable yet


## Table of Contents
- [Installation :computer:](#installation-computer)
- [Getting Started :chart_with_upwards_trend:](#getting-started-chart_with_upwards_trend)
    * [Flask Application (by petisco :cookie:)](#flask-application-by-petisco-cookie)
    * [Configure your Application :rocket:](#configure-your-application-rocket)
    * [Logging](#logging)
    * [Handlers](#handlers)
      - [Controller Handler](#controller-handler)
    * [Model your Domain](#model-your-domain)
      - [Value Objects](#value-objects)
      - [Aggregate Root](#aggregate-root)
      - [Events](#events)
      - [Webhooks](#webhooks)
- [Testing :white_check_mark:](#testing-white_check_mark)
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
pip install petisco[fixtures]
pip install petisco[flask,sqlalchemy,redis,rabbitmq,fixtures]
```

## Getting Started :chart_with_upwards_trend:	

### Flask Application (by Petisco :cookie:)

Check the following repo to learn how to use petisco with flask: [petisco-task-manager](https://github.com/alice-biometrics/petisco-task-manager)

### Configure your Application :rocket:

Configure your app using the `petisco.yml`

```yaml
app:
  name: taskmanager
  version:
    from_file: VERSION
tasks:
  recurring-task:
    run_in: 5 # seconds
    interval: 10 # seconds
    handler: taskmanager.tasks.recurring_task
  scheduled-task:
    run_in: 10 # seconds
    handler: taskmanager.tasks.scheduled_task
  instant-task:
    handler: taskmanager.tasks.instant_task
framework:
    selected_framework: flask
    config_file: swagger.yaml
    port: 8080
    port_env: PETISCO_PORT
logger:
    selected_logger: logging
    name: petisco
    format: "%(name)s - %(levelname)s - %(message)s"
    config: taskmanager.src.config.logging.logging_config
persistence:
  config: taskmanager.src.config.persistence.config_persistence
  models:
    task: taskmanager.src.modules.tasks.infrastructure.persistence.models.task_model.TaskModel
    event: taskmanager.src.modules.events.infrastructure.persistence.models.event_model.EventModel
providers:
   services_provider: taskmanager.src.config.services.services_provider
   repositories_provider: taskmanager.src.config.repositories.repositories_provider
events:
  publish_deploy_event: True
  publisher:
    provider: taskmanager.src.config.events.publisher_provider
  subscriber:
    provider: taskmanager.src.config.events.subscriber_provider
    subscribers:
      store-event:
        organization: acme
        service: taskmanager
        topic: taskmanager-events
        dead_letter: True
        handler: taskmanager.src.modules.events.application.store.event_store.event_store
```

For instance, if your app don't need cron dispatchers, events persistence and repositories, you can remove it from the `petisco.yml`:

```yaml
app:
  name: taskmanager-nopersistence
  version:
    from_file: VERSION
framework:
    selected_framework: flask
    config_file: swagger.yaml
    port: 8080
    port_env: PETISCO_PORT
logger:
    selected_logger: logging
    name: petisco
    format: "%(name)s - %(levelname)s - %(message)s"
    config: taskmanager.src.config.logging.logging_config
providers:
   services_provider: taskmanager.src.config.services.services_provider
```

### Logging

If you use a logging-based logger

```yaml
logger:
    selected_logger: logging # <---
    name: petisco
    format: "%(name)s - %(levelname)s - %(message)s"
    config: taskmanager.src.config.logging.logging_config
```

You can set logging level with the environment variable `PETISCO_LOGGING_LEVEL`.

Options:

```
PETISCO_LOGGING_LEVEL: DEBUG
PETISCO_LOGGING_LEVEL: INFO
PETISCO_LOGGING_LEVEL: WARNING
PETISCO_LOGGING_LEVEL: ERROR
PETISCO_LOGGING_LEVEL: CRITICAL
```

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
        Application Name. If not specified it will get it from Petisco.get_app_version().
    app_version
        Application Version. If not specified it will get it from Petisco.get_app_version().
    logger
        A ILogger implementation. If not specified it will get it from Petisco.get_logger(). You can also use NotImplementedLogger
    token_manager
        TokenManager object. Here, you can define how to deal with JWT Tokens
    success_handler
        Handler to deal with Success Results
    error_handler
        Handler to deal with Failure Results
    headers_provider
        Injectable function to provide headers. By default is used headers_provider
    logging_types_blacklist
        Logging Blacklist. Object of defined Type will not be logged. By default ( [bytes] ) bytes object won't be logged.
    publisher
        A IEventPublisher implementation. If not specified it will get it from Petisco.get_event_publisher().
    send_request_responded_event
        Boolean to select if RequestResponded event is send. It will use provided publisher
    """
    
### Model your Domain


#### Value Objects

Extend `ValueObject` to model your Value Objects.

Find some examples in [petisco/domain/value_objects](petisco/domain/value_objects)

#### Aggregate Root

Extend `AggregateRoot` to model your Aggregate Roots
 
```python
from petisco import AggregateRoot, UserId, Name
from my_code import UserCreated

class User(AggregateRoot):

    def __init__(self, name: Name, user_id: UserId):
        self.name = name
        self.user_id = user_id
        super().__init__()

    @staticmethod
    def create(name: Name):
        user = User(name, UserId.generate())
        user.record(UserCreated(user.user_id, user.name))
        return user
```

Use semantic constructors and `record` domain `Event`s very easy.

```python 
user = User.create(Name("Petisco"))
events = user.pull_domain_events() # Events ready to be published
```

#### Events

Extend `Event` to model your domain events.

```python
from petisco import Event, UserId, Name

class UserCreated(Event):
    user_id: UserId
    name: Name

    def __init__(self, user_id: UserId, name: Name):
        self.user_id = user_id
        self.name = name
        super().__init__()
```

To prevent the propagation of Id parameters throughout your domain, you can compose your Event with a [`InfoId`](petisco/domain/aggregate_roots/info_id.py)

```python
user_created = UserCreated(user_id, name).add_info_id(info_id)
```

How can we publish and consume events?

* We publish events using an `EventBus`, and
* Consume events using an `EventConsumer`.

To learn more about this topic, and how to configure it, please take a look to [EventManagement](doc/events/EventManagement.md) documentation.

#### Webhooks

Create your webhooks easily with `Webhook` class. 

Check how to use it with a simple example:

1. Run a [service](examples/webhooks/subscribed_app.py) that will expose an entry point where webhooks will be attended:
    ```console
    export FLASK_APP=examples/webhooks/subscribed_app.py; python -m flask run
    ```
2. Execute a [Webhook](examples/webhooks/execute_webhook.py):
     ```console
    python examples/webhooks/execute_webhook.py
    ```


### Testing :white_check_mark:

###### Petisco Fixtures

Import useful petisco fixtures with :

```python
from petisco.fixtures import *
```

We can use [petisco_client](petisco/fixtures/client.py) to simulate our client in acceptance tests

```python
import pytest

@pytest.mark.acceptance
@pytest.mark.persistence_source("acme")
def test_should_return_200_when_call_healthcheck(
    petisco_client
):
    response = petisco_client.get("/petisco/environment")
    assert response.status_code == 200
```

Included in *petisco_client* we can find [petisco_sql_database](petisco/fixtures/persistence.py).
This fixture will create and connect a database and after the test this will be deleted.

Note that to use these fixtures you must indicate with a marker the persistence source. In the above example the 
persistence source is named `acme`.


#### Extras

###### RabbitMQ <img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/rabbitmq.png" width="16">

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
