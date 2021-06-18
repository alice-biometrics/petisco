# coding=utf-8
# Legacy module of petisco version 0

from petisco.legacy.controller.errors.internal_http_error import InternalHttpError

# Classes
from petisco.legacy.application.app_services import AppServices, AppService
from petisco.legacy.application.config.config import Config
from petisco.legacy.application.interface_repository import IRepository
from petisco.legacy.application.repositories import Repositories, Repository
from petisco.legacy.application.interface_app_service import IService, IAppService
from petisco.legacy.application.petisco import Petisco
from petisco.legacy.application.singleton import Singleton
from petisco.legacy.domain.aggregate_roots.aggregate_root import AggregateRoot
from petisco.legacy.domain.aggregate_roots.info_id import InfoId
from petisco.legacy.domain.date_parser import DateParser
from petisco.legacy.domain.errors.empty_value_object_error import EmptyValueObjectError
from petisco.legacy.domain.errors.length_limit_string_value_object_error import (
    ExceedLengthLimitValueObjectError,
    NotReachMinimumValueObjectError,
    NotHasSpecificLengthValueObjectError,
)
from petisco.legacy.domain.errors.given_name_is_not_valid_error import (
    GivenNameIsNotValidError,
)
from petisco.legacy.domain.errors.unknown_error import UnknownError
from petisco.legacy.domain.value_objects.integer_value_object import IntegerValueObject
from petisco.legacy.domain.value_objects.name import Name
from petisco.legacy.domain.value_objects.client_id import ClientId
from petisco.legacy.domain.value_objects.string_value_object import (
    StringValueObject,
    InvalidStringValueObjectError,
)
from petisco.legacy.domain.value_objects.user_id import UserId
from petisco.legacy.domain.value_objects.correlation_id import CorrelationId
from petisco.legacy.domain.value_objects.uuid import Uuid, InvalidUuidError
from petisco.legacy.domain.value_objects.value_object import (
    ValueObject,
    value_object_field,
)
from petisco.legacy.event.bus.domain.interface_event_bus import IEventBus
from petisco.legacy.event.chaos.domain.interface_event_chaos import IEventChaos
from petisco.legacy.event.handler.event_handler import event_handler
from petisco.legacy.frameworks.interface_application import IApplication
from petisco.legacy.http.request import Request
from petisco.legacy.http.request_errors import (
    MultipartFormatRequestError,
    MissingSchemaRequestError,
    TimeoutRequestError,
    ConnectionRequestError,
    UnknownRequestError,
    UnauthorizedRequestError,
    BadRequestError,
)
from petisco.legacy.http.response import Response
from petisco.legacy.logger.log_message import LogMessage
from petisco.legacy.logger.logging_based_logger import LoggingBasedLogger
from petisco.legacy.logger.interface_logger import ILogger
from petisco.legacy.notifier.domain.interface_notifier import INotifier
from petisco.legacy.notifier.domain.notifier_message import NotifierMessage
from petisco.legacy.notifier.infrastructure.not_implemented_notifier import (
    NotImplementedNotifier,
)
from petisco.legacy.security.token_decoder.interface_token_decoder import ITokenDecoder
from petisco.legacy.security.token_decoder.token_decoder import TokenDecoder
from petisco.legacy.security.token_manager.accepted_token import AcceptedToken
from petisco.legacy.security.token_manager.interface_token_manager import ITokenManager
from petisco.legacy.security.token_manager.not_implemented_token_manager import (
    NotImplementedTokenManager,
)
from petisco.legacy.security.token_manager.token_manager import TokenManager
from petisco.legacy.tools.pool_executor import PoolExecutor, Executable
from petisco.legacy.use_case import UseCase
from petisco.legacy.use_case import use_case_handler
from petisco.legacy.controller.controller_handler import controller_handler
from petisco.legacy.controller.errors.http_error import (
    HttpError,
    DEFAULT_HTTP_ERROR_MESSAGE,
)

from petisco.legacy.event.shared.domain.event import Event, Events, unique_events
from petisco.legacy.event.shared.domain.event_id import EventId, InvalidEventIdError

# Legacy Events
from petisco.legacy.event.legacy.publisher.domain.interface_event_publisher import (
    IEventPublisher,
)
from petisco.legacy.event.legacy.publisher.infrastructure.not_implemented_event_publisher import (
    NotImplementedEventPublisher,
)
from petisco.legacy.event.legacy.routing_key import RoutingKey
from petisco.legacy.event.legacy.subscriber.domain.config_event_subscriber import (
    ConfigEventSubscriber,
)
from petisco.legacy.event.legacy.subscriber.domain.interface_event_subscriber import (
    IEventSubscriber,
)
from petisco.legacy.event.legacy.subscriber.domain.subscriber_handler import (
    subscriber_handler,
)
from petisco.legacy.event.legacy.subscriber.infrastructure.not_implemented_event_subscriber import (
    NotImplementedEventSubscriber,
)
from petisco.legacy.event.shared.domain.event_subscriber import EventSubscriber
from petisco.legacy.webhooks.webhook.domain.secret import SecretIsNotHexError, Secret
from petisco.legacy.webhooks.webhook.domain.signature_algorithm import (
    SignatureAlgorithm,
)
from petisco.legacy.webhooks.webhook.domain.webhook import Webhook
from petisco.legacy.webhooks.webhook.domain.webhook_sender_failed import (
    WebhookSenderFailed,
)
from petisco.legacy.webhooks.webhook.domain.webhook_result_id import WebhookResultId
from petisco.legacy.webhooks.webhook.domain.webhook_id import WebhookId
from petisco.legacy.webhooks.webhook.domain.webhook_result import WebhookResult
from petisco.legacy.webhooks.webhook.domain.webhook_sender import WebhookSender

classes = [
    "IService",  # deprecated
    "IAppService",
    "AppService",
    "AppServices",
    "IRepository",
    "Repository",
    "Repositories",
    "UseCase",
    "use_case_handler",
    "controller_handler",
    "CorrelationId",
    "HttpError",
    "InternalHttpError",
    "LoggingBasedLogger",
    "ILogger",
    "Event",
    "RoutingKey",
    "Events",
    "EventId",
    "InvalidEventIdError",
    "unique_events",
    "Singleton",
    "TokenManager",
    "AcceptedToken",
    "NotImplementedTokenManager",
    "ITokenManager",
    "TokenDecoder",
    "ITokenDecoder",
    "ValueObject",
    "Name",
    "ClientId",
    "UserId",
    "Uuid",
    "StringValueObject",
    "IntegerValueObject",
    "InvalidUuidError",
    "InvalidStringValueObjectError",
    "GivenNameIsNotValidError",
    "UnknownError",
    "InfoId",
    "AggregateRoot",
    "Petisco",
    "IApplication",
    "Config",
    "EmptyValueObjectError",
    "ExceedLengthLimitValueObjectError",
    "NotReachMinimumValueObjectError",
    "EventSubscriber",
    "subscriber_handler",
    "ConfigEventSubscriber",
    "IEventPublisher",
    "IEventSubscriber",
    "NotImplementedEventPublisher",
    "NotImplementedEventSubscriber",
    "INotifier",
    "NotImplementedNotifier",
    "NotifierMessage",
    "LogMessage",
    "Request",
    "Response",
    "MultipartFormatRequestError",
    "MissingSchemaRequestError",
    "TimeoutRequestError",
    "ConnectionRequestError",
    "UnknownRequestError",
    "UnauthorizedRequestError",
    "BadRequestError",
    "IEventBus",
    "event_handler",
    "Webhook",
    "WebhookSender",
    "WebhookId",
    "WebhookResult",
    "WebhookResultId",
    "WebhookSenderFailed",
    "IEventChaos",
    "SecretIsNotHexError",
    "NotHasSpecificLengthValueObjectError",
    "Secret",
    "SignatureAlgorithm",
    "DateParser",
    "value_object_field",
    "PoolExecutor",
    "Executable",
    "DEFAULT_HTTP_ERROR_MESSAGE",
]

from petisco.legacy.persistence.fake_database import FakeDatabase
from petisco.legacy.persistence.interface_database import IDatabase
from petisco.legacy.persistence.interface_persistence_connector import (
    IPersistenceConnector,
)
from petisco.legacy.persistence.persistence import Persistence
from petisco.legacy.persistence.persistence_models import PersistenceModels
from petisco.legacy.persistence.sql.errors import (
    ClientNotFoundError,
    ClientAlreadyExistError,
    UserNotFoundError,
    UserAlreadyExistError,
    EntityAlreadyExistError,
    EntityNotFoundError,
    EntitiesNotFoundError,
)

persistence = [
    "Persistence",
    "IDatabase",
    "FakeDatabase",
    "PersistenceModels",
    "IPersistenceConnector",
    "ClientNotFoundError",
    "ClientAlreadyExistError",
    "UserNotFoundError",
    "UserAlreadyExistError",
    "EntityAlreadyExistError",
    "EntityNotFoundError",
    "EntitiesNotFoundError",
]


# Controllers & Use Cases
from petisco.legacy.modules.environment.application.environment import environment
from petisco.legacy.modules.environment.application.environment_provider import (
    EnvironmentProvider,
)
from petisco.legacy.modules.environment.domain.environment_provider_error import (
    EnvironmentProviderError,
)
from petisco.legacy.modules.healthcheck.application.healthcheck import healthcheck
from petisco.legacy.modules.healthcheck.application.healthcheck_provider import (
    HealthcheckProvider,
)
from petisco.legacy.modules.healthcheck.domain.persistence_error import PersistenceError

controllers_and_use_cases = [
    "environment",
    "EnvironmentProvider",
    "EnvironmentProviderError",
    "healthcheck",
    "HealthcheckProvider",
    "PersistenceError",
]

# Constants
from petisco.legacy.logger.interface_logger import (
    CRITICAL,
    FATAL,
    ERROR,
    WARNING,
    WARN,
    INFO,
    DEBUG,
    NOTSET,
)

constants = ["CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"]

# Flask
try:
    from petisco.legacy.frameworks.flask.application.flask_application import (
        FlaskApplication,
    )

    flask = ["FlaskApplication"]
except (RuntimeError, ImportError):
    flask = []

# SqlAlchemy
try:
    from petisco.legacy.persistence.sqlalchemy.sqlalchemy_operational_database_error import (
        SqlAlchemyOperationalDatabaseError,
    )
    from petisco.legacy.persistence.sql.sqlite.sqlite_connection import SqliteConnection
    from petisco.legacy.persistence.sql.sqlite.sqlite_database import SqliteDatabase
    from petisco.legacy.persistence.sql.mysql.mysql_connection import MySqlConnection
    from petisco.legacy.persistence.sql.mysql.mysql_database import MySqlDatabase
    from petisco.legacy.persistence.sql.sql_repository import SqlRepository
    from petisco.legacy.persistence.sql.sql_executor import SqlExecutor

    sql = [
        "SqlAlchemyOperationalDatabaseError",
        "SqliteConnection",
        "SqliteDatabase",
        "MySqlConnection",
        "MySqlDatabase",
        "SqlRepository",
        "SqlExecutor",
    ]
except (RuntimeError, ImportError):
    sql = []

# PyMongo
try:
    from petisco.legacy.persistence.pymongo.pymongo_persistence import (
        PyMongoPersistence,
    )
    from petisco.legacy.persistence.pymongo.pymongo_persistence_config import (
        PyMongoPersistenceConfig,
    )
    from petisco.legacy.persistence.pymongo.pymongo_persistence_connector import (
        PyMongoPersistenceConnector,
    )
    from petisco.legacy.persistence.pymongo.pymongo_errors import (
        PyMongoOperationalDatabaseError,
        PyMongoInvalidDatabaseNameError,
        PyMongoInvalidCollectionNameError,
    )
    from petisco.legacy.persistence.pymongo.pymongo_persistence_context import (
        get_mongo_collection,
    )

    pymongo = [
        "PyMongoPersistence",
        "PyMongoPersistenceConfig",
        "PyMongoPersistenceConnector",
        "PyMongoInvalidCollectionNameError",
        "PyMongoInvalidDatabaseNameError",
        "PyMongoInvalidCollectionNameError",
        "get_mongo_collection",
    ]
except (RuntimeError, ImportError):
    pymongo = []


# Elastic
try:
    from petisco.legacy.persistence.elastic.elastic_connection import ElasticConnection
    from petisco.legacy.persistence.elastic.elastic_database import ElasticDatabase

    elastic = ["ElasticConnection", "ElasticDatabase"]
except (RuntimeError, ImportError):
    elastic = []

# RabbitMQ
try:
    from petisco.legacy.event.shared.infrastructure.rabbitmq.rabbitmq_connector import (
        RabbitMqConnector,
    )
    from petisco.legacy.event.configurer.infrastructure.rabbitmq_event_configurer import (
        RabbitMqEventConfigurer,
    )

    from petisco.legacy.event.consumer.infrastructure.rabbitmq_event_consumer import (
        RabbitMqEventConsumer,
    )

    from petisco.legacy.event.chaos.infrastructure.rabbitmq_event_chaos import (
        RabbitMqEventChaos,
    )

    # deprecated
    from petisco.legacy.event.legacy.publisher.infrastructure.rabbitmq_event_publisher import (
        RabbitMQEventPublisher,
    )
    from petisco.legacy.event.legacy.subscriber.infrastructure.rabbitmq_event_subscriber import (
        RabbitMQEventSubscriber,
    )
    from petisco.legacy.event.bus.infrastructure.rabbitmq_event_bus import (
        RabbitMqEventBus,
    )

    rabbitmq = [
        "RabbitMQEventPublisher",
        "RabbitMQEventSubscriber",
        "RabbitMqConnector",
        "RabbitMqEventConfigurer",
        "RabbitMqEventConsumer",
        "RabbitMqEventBus",
        "RabbitMqEventChaos",
    ]
except (RuntimeError, ImportError):
    rabbitmq = []

# Slack
try:
    from petisco.legacy.notifier.infrastructure.slack.slack_notifier import (
        SlackNotifier,
    )

    slack = ["SlackNotifier"]
except (RuntimeError, ImportError):
    slack = []

__all__ = (
    classes
    + persistence
    + controllers_and_use_cases
    + constants
    + flask
    + sql
    + pymongo
    + elastic
    + rabbitmq
    + slack
)
