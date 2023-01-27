
## Middleware

| Envvar                        | Default                             | Options                   | Description    |  
|-------------------------------|-------------------------------------|---------------------------|----------------|
| `PETISCO_DEFAULT_MIDDLEWARES` | NotifierMiddleware,PrintMiddleware  | Registered implementation | Define default |


## Dependencies


| Install                           | Default  | Options         | Description                                                             |  
|-----------------------------------|----------|-----------------|-------------------------------------------------------------------------|
| `PETISCO_NOTIFIER_TYPE`           | slack    | not_implemented | Set the notifier implementation                                         |
| `PETISCO_DOMAIN_EVENT_BUS_TYPE`   | rabbitmq | not_implemented | Set the DomainEventBus implementation                                   |
| `PETISCO_COMMAND_BUS_TYPE`        | rabbitmq | not_implemented | Set the CommandBus implementation                                       |
| `PETISCO_MESSAGE_CONFIGURER_TYPE` | rabbitmq | not_implemented | Set the implementation of the message broker configuration              |
| `PETISCO_MESSAGE_CONSUMER_TYPE`   | rabbitmq | not_implemented | Set the implementation of the message broker consumer (add subscribers) |




## RabbitMQ

| Install                                               | Default | Options | Description                                                                       |  
|-------------------------------------------------------|---------|---------|-----------------------------------------------------------------------------------|
| `PETISCO_RABBITMQ_CONFIGURER_CLEAR_SUBSCRIBER_BEFORE` | false   | bool    |                                                                                   |
| `PETISCO_RABBITMQ_CONFIGURER_CLEAR_STORE_BEFORE`      | false   | bool    |                                                                                   |
| `PETISCO_RABBITMQ_MAX_ATTEMPTS_TO_RECONNECT_CONSUMER` | 20      | int     | Set max number of attempt to try to reconnect rabbitmq channel in the consumer    |
| `PETISCO_RABBITMQ_WAIT_SECONDS_TO_RECONNECT_CONSUMER` | 5       | int     | Set wait time (in seconds) to retry to reconnect rabbitmq channel in the consumer |

