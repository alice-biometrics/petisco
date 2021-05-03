# coding=utf-8
# Copyright (C) 2019+ Alice, Vigo, Spain

"""Public API of ALiCE Petisco Framework"""

# Classes
from petisco.application.app_services import AppServices, AppService
from petisco.application.config.config import Config
from petisco.application.interface_repository import IRepository
from petisco.application.repositories import Repositories, Repository
from petisco.application.interface_app_service import IService, IAppService
from petisco.application.petisco import Petisco
from petisco.application.singleton import Singleton
from petisco.domain.aggregate_roots.aggregate_root import AggregateRoot
from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.domain.date_parser import DateParser
from petisco.domain.errors.empty_value_object_error import EmptyValueObjectError
from petisco.domain.errors.length_limit_string_value_object_error import (
    ExceedLengthLimitValueObjectError,
    NotReachMinimumValueObjectError,
    NotHasSpecificLengthValueObjectError,
)
from petisco.domain.errors.given_name_is_not_valid_error import GivenNameIsNotValidError
from petisco.domain.errors.unknown_error import UnknownError
from petisco.domain.value_objects.integer_value_object import IntegerValueObject
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.string_value_object import (
    StringValueObject,
    InvalidStringValueObjectError,
)
from petisco.domain.value_objects.user_id import UserId
from petisco.domain.value_objects.correlation_id import CorrelationId
from petisco.domain.value_objects.uuid import Uuid, InvalidUuidError
from petisco.domain.value_objects.value_object import ValueObject, value_object_field
from petisco.event.bus.domain.interface_event_bus import IEventBus
from petisco.event.chaos.domain.interface_event_chaos import IEventChaos
from petisco.event.handler.event_handler import event_handler
from petisco.frameworks.interface_application import IApplication
from petisco.http.request import Request
from petisco.http.request_errors import (
    MultipartFormatRequestError,
    MissingSchemaRequestError,
    TimeoutRequestError,
    ConnectionRequestError,
    UnknownRequestError,
    UnauthorizedRequestError,
    BadRequestError,
)
from petisco.http.response import Response
from petisco.logger.log_message import LogMessage
from petisco.logger.logging_based_logger import LoggingBasedLogger
from petisco.logger.interface_logger import ILogger
from petisco.notifier.domain.interface_notifier import INotifier
from petisco.notifier.domain.notifier_message import NotifierMessage
from petisco.notifier.infrastructure.not_implemented_notifier import (
    NotImplementedNotifier,
)
from petisco.security.token_decoder.interface_token_decoder import ITokenDecoder
from petisco.security.token_decoder.token_decoder import TokenDecoder
from petisco.security.token_manager.accepted_token import AcceptedToken
from petisco.security.token_manager.interface_token_manager import ITokenManager
from petisco.security.token_manager.not_implemented_token_manager import (
    NotImplementedTokenManager,
)
from petisco.security.token_manager.token_manager import TokenManager
from petisco.tools.pool_executor import PoolExecutor, Executable
from petisco.use_case import UseCase
from petisco.use_case import use_case_handler
from petisco.controller.controller_handler import controller_handler
from petisco.controller.errors.http_error import HttpError

from petisco.event.shared.domain.event import Event, Events, unique_events
from petisco.event.shared.domain.event_id import EventId, InvalidEventIdError

# Legacy Events
from petisco.event.legacy.publisher.domain.interface_event_publisher import (
    IEventPublisher,
)
from petisco.event.legacy.publisher.infrastructure.not_implemented_event_publisher import (
    NotImplementedEventPublisher,
)
from petisco.event.legacy.routing_key import RoutingKey
from petisco.event.legacy.subscriber.domain.config_event_subscriber import (
    ConfigEventSubscriber,
)
from petisco.event.legacy.subscriber.domain.interface_event_subscriber import (
    IEventSubscriber,
)
from petisco.event.legacy.subscriber.domain.subscriber_handler import subscriber_handler
from petisco.event.legacy.subscriber.infrastructure.not_implemented_event_subscriber import (
    NotImplementedEventSubscriber,
)
from petisco.event.shared.domain.event_subscriber import EventSubscriber
from petisco.webhooks.webhook.domain.secret import SecretIsNotHexError, Secret
from petisco.webhooks.webhook.domain.signature_algorithm import SignatureAlgorithm
from petisco.webhooks.webhook.domain.webhook import Webhook
from petisco.webhooks.webhook.domain.webhook_sender_failed import WebhookSenderFailed
from petisco.webhooks.webhook.domain.webhook_result_id import WebhookResultId
from petisco.webhooks.webhook.domain.webhook_id import WebhookId
from petisco.webhooks.webhook.domain.webhook_result import WebhookResult
from petisco.webhooks.webhook.domain.webhook_sender import WebhookSender

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
]

from petisco.persistence.fake_database import FakeDatabase
from petisco.persistence.interface_database import IDatabase
from petisco.persistence.interface_persistence_connector import IPersistenceConnector
from petisco.persistence.persistence import Persistence
from petisco.persistence.persistence_models import PersistenceModels
from petisco.persistence.sql.errors import (
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
from petisco.modules.environment.application.environment import environment
from petisco.modules.environment.application.environment_provider import (
    EnvironmentProvider,
)
from petisco.modules.environment.domain.environment_provider_error import (
    EnvironmentProviderError,
)
from petisco.modules.healthcheck.application.healthcheck import healthcheck
from petisco.modules.healthcheck.application.healthcheck_provider import (
    HealthcheckProvider,
)
from petisco.modules.healthcheck.domain.persistence_error import PersistenceError

controllers_and_use_cases = [
    "environment",
    "EnvironmentProvider",
    "EnvironmentProviderError",
    "healthcheck",
    "HealthcheckProvider",
    "PersistenceError",
]

# Constants
from petisco.logger.interface_logger import (
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
    from petisco.frameworks.flask.application.flask_application import FlaskApplication

    flask = ["FlaskApplication"]
except (RuntimeError, ImportError):
    flask = []

# SqlAlchemy
try:
    from petisco.persistence.sqlalchemy.sqlalchemy_operational_database_error import (
        SqlAlchemyOperationalDatabaseError,
    )
    from petisco.persistence.sql.sqlite.sqlite_connection import SqliteConnection
    from petisco.persistence.sql.sqlite.sqlite_database import SqliteDatabase
    from petisco.persistence.sql.mysql.mysql_connection import MySqlConnection
    from petisco.persistence.sql.mysql.mysql_database import MySqlDatabase
    from petisco.persistence.sql.sql_repository import SqlRepository
    from petisco.persistence.sql.sql_executor import SqlExecutor

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
    from petisco.persistence.pymongo.pymongo_persistence import PyMongoPersistence
    from petisco.persistence.pymongo.pymongo_persistence_config import (
        PyMongoPersistenceConfig,
    )
    from petisco.persistence.pymongo.pymongo_persistence_connector import (
        PyMongoPersistenceConnector,
    )
    from petisco.persistence.pymongo.pymongo_errors import (
        PyMongoOperationalDatabaseError,
        PyMongoInvalidDatabaseNameError,
        PyMongoInvalidCollectionNameError,
    )
    from petisco.persistence.pymongo.pymongo_persistence_context import (
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
    from petisco.persistence.elastic.elastic_connection import ElasticConnection
    from petisco.persistence.elastic.elastic_database import ElasticDatabase

    elastic = ["ElasticConnection", "ElasticDatabase"]
except (RuntimeError, ImportError):
    elastic = []

# RabbitMQ
try:
    from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_connector import (
        RabbitMqConnector,
    )
    from petisco.event.configurer.infrastructure.rabbitmq_event_configurer import (
        RabbitMqEventConfigurer,
    )

    from petisco.event.consumer.infrastructure.rabbitmq_event_consumer import (
        RabbitMqEventConsumer,
    )

    from petisco.event.chaos.infrastructure.rabbitmq_event_chaos import (
        RabbitMqEventChaos,
    )

    # deprecated
    from petisco.event.legacy.publisher.infrastructure.rabbitmq_event_publisher import (
        RabbitMQEventPublisher,
    )
    from petisco.event.legacy.subscriber.infrastructure.rabbitmq_event_subscriber import (
        RabbitMQEventSubscriber,
    )
    from petisco.event.bus.infrastructure.rabbitmq_event_bus import RabbitMqEventBus

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
    from petisco.notifier.infrastructure.slack.slack_notifier import SlackNotifier

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
