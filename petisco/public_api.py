# coding=utf-8
# Copyright (C) 2019+ Alice, Vigo, Spain

"""Public API of ALiCE Petisco Framework"""

# Classes
from petisco.application.application_config import ApplicationConfig
from petisco.application.repository import Repository
from petisco.application.service import Service
from petisco.application.singleton import Singleton
from petisco.commands.command_handler import command_handler
from petisco.controller.correlation_id import CorrelationId
from petisco.controller.tokens.jwt_config import JwtConfig
from petisco.domain.entities.client_id import ClientId
from petisco.domain.entities.name import Name
from petisco.domain.entities.user_id import UserId
from petisco.events.event_config import EventConfig
from petisco.logger.logging_based_logger import LoggingBasedLogger
from petisco.logger.interface_logger import ILogger
from petisco.persistence.interface_persistence_connector import IPersistenceConnector
from petisco.use_case import UseCase
from petisco.use_case import use_case_handler
from petisco.controller.controller_handler import controller_handler
from petisco.controller.errors.http_error import HttpError
from petisco.events.event import Event
from petisco.events.event_id import EventId
from petisco.events.interface_event_manager import IEventManager
from petisco.events.not_implemented_event_manager import NotImplementedEventManager

classes = [
    "ApplicationConfig",
    "Service",
    "Repository",
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
    "JwtConfig",
    "IPersistenceConnector",
    "Name",
    "ClientId",
    "UserId",
    "EventConfig",
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

__all__ = classes + constants + flask + sqlalchemy + redis + rabbitmq
