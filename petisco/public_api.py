# coding=utf-8
# Copyright (C) 2019+ Alice, Vigo, Spain

"""Public API of ALiCE Petisco Framework"""

# Classes

from petisco.application.config.config import Config
from petisco.application.interface_repository import IRepository
from petisco.application.interface_service import IService
from petisco.application.petisco import Petisco
from petisco.application.singleton import Singleton
from petisco.commands.command_handler import command_handler
from petisco.domain.aggregate_roots.aggregate_root import AggregateRoot
from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.domain.errors.empty_value_object_error import EmptyValueObjectError
from petisco.domain.errors.exceed_length_limit_value_error_error import (
    ExceedLengthLimitValueObjectError,
)
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.user_id import UserId
from petisco.domain.value_objects.correlation_id import CorrelationId
from petisco.domain.value_objects.value_object import ValueObject
from petisco.events.event_config import EventConfig
from petisco.frameworks.interface_application import IApplication
from petisco.logger.logging_based_logger import LoggingBasedLogger
from petisco.logger.interface_logger import ILogger
from petisco.persistence.interface_persistence_connector import IPersistenceConnector
from petisco.security.token_decoder.interface_token_decoder import ITokenDecoder
from petisco.security.token_decoder.token_decoder import TokenDecoder
from petisco.security.token_manager.interface_token_manager import ITokenManager
from petisco.security.token_manager.not_implemented_token_manager import (
    NotImplementedTokenManager,
)
from petisco.security.token_manager.token_manager import TokenManager
from petisco.use_case import UseCase
from petisco.use_case import use_case_handler
from petisco.controller.controller_handler import controller_handler
from petisco.controller.errors.http_error import HttpError
from petisco.events.event import Event
from petisco.events.event_id import EventId
from petisco.events.interface_event_manager import IEventManager
from petisco.events.not_implemented_event_manager import NotImplementedEventManager

classes = [
    "IService",
    "IRepository",
    "UseCase",
    "use_case_handler",
    "controller_handler",
    "command_handler",
    "CorrelationId",
    "HttpError",
    "LoggingBasedLogger",
    "ILogger",
    "Event",
    "EventId",
    "IEventManager",
    "NotImplementedEventManager",
    "Singleton",
    "TokenManager",
    "NotImplementedTokenManager",
    "ITokenManager",
    "TokenDecoder",
    "ITokenDecoder",
    "IPersistenceConnector",
    "ValueObject",
    "Name",
    "ClientId",
    "UserId",
    "InfoId",
    "EventConfig",
    "AggregateRoot",
    "Petisco",
    "IApplication",
    "Config",
    "EmptyValueObjectError",
    "ExceedLengthLimitValueObjectError",
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
    from petisco.persistence.sqlalchemy.sqlalchemy_persistence import (
        SqlAlchemyPersistence,
    )
    from petisco.persistence.sqlalchemy.sqlalchemy_persistence_config import (
        SqlAlchemyPersistenceConfig,
    )
    from petisco.persistence.sqlalchemy.sqlalchemy_persistence_connector import (
        SqlAlchemyPersistenceConnector,
    )
    from petisco.persistence.sqlalchemy.sqlalchemy_session_scope import session_scope
    from petisco.persistence.sqlalchemy.sqlalchemy_operational_database_error import (
        SqlAlchemyOperationalDatabaseError,
    )

    sqlalchemy = [
        "SqlAlchemyPersistence",
        "SqlAlchemyPersistenceConfig",
        "SqlAlchemyPersistenceConnector",
        "session_scope",
        "SqlAlchemyOperationalDatabaseError",
    ]
except (RuntimeError, ImportError):
    sqlalchemy = []

# Redis
try:
    from petisco.events.redis.redis_event_manager import RedisEventManager
    from petisco.events.redis.event_from_redis_message import (
        event_from_redis_message,
        EventFromRedisMessageConversionError,
    )

    redis = [
        "RedisEventManager",
        "event_from_redis_message",
        "EventFromRedisMessageConversionError",
    ]
except (RuntimeError, ImportError):
    redis = []

# RabbitMq
try:
    from petisco.events.rabbitmq.rabbitmq_event_manager import RabbitMQEventManager

    rabbitmq = ["RabbitMQEventManager"]
except (RuntimeError, ImportError):
    rabbitmq = []

__all__ = (
    classes
    + controllers_and_use_cases
    + constants
    + flask
    + sqlalchemy
    + redis
    + rabbitmq
)
