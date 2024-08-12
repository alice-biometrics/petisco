"""Public API of Alice Petisco Framework"""

from petisco.base.application.application import Application
from petisco.base.application.application_configurer import ApplicationConfigurer
from petisco.base.application.controller.async_controller import AsyncController
from petisco.base.application.controller.controller import Controller
from petisco.base.application.controller.error_map import ErrorMap
from petisco.base.application.controller.handlers import (
    custom_message_handler,
    unwrap_result_handler,
)
from petisco.base.application.controller.http_error import HttpError
from petisco.base.application.dependency_injection.container import Container
from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.application.middleware.middleware import Middleware
from petisco.base.application.middleware.notifier_middleware import NotifierMiddleware
from petisco.base.application.middleware.print_middleware import PrintMiddleware
from petisco.base.application.notifier.not_implemented_notifier import (
    NotImplementedNotifier,
)
from petisco.base.application.notifier.notifier import Notifier
from petisco.base.application.notifier.notifier_exception_message import (
    NotifierExceptionMessage,
)
from petisco.base.application.notifier.notifier_message import NotifierMessage
from petisco.base.application.patterns.app_service import AppService
from petisco.base.application.patterns.async_app_service import AsyncAppService
from petisco.base.application.patterns.crud_repository import CrudRepository
from petisco.base.application.patterns.inmemory_crud_repository import (
    InmemoryCrudRepository,
)
from petisco.base.application.patterns.repository import Repository
from petisco.base.application.use_case.async_use_case import AsyncUseCase
from petisco.base.application.use_case.use_case import UseCase
from petisco.base.application.use_case.use_case_uncontrolled_error import (
    UseCaseUncontrolledError,
)
from petisco.base.domain.errors.critical_error import CriticalError
from petisco.base.domain.errors.default_http_error_map import DEFAULT_HTTP_ERROR_MAP
from petisco.base.domain.errors.defaults.already_exists import (
    AggregateAlreadyExistError,
    AlreadyExists,
    ClientAlreadyExists,
    UserAlreadyExists,
)
from petisco.base.domain.errors.defaults.bus import BusCannotPublish
from petisco.base.domain.errors.defaults.invalid_uuid import InvalidUuid
from petisco.base.domain.errors.defaults.invalid_value_object import InvalidValueObject
from petisco.base.domain.errors.defaults.not_allowed import NotAllowed
from petisco.base.domain.errors.defaults.not_found import (
    AggregateNotFoundError,
    AggregatesNotFoundError,
    ClientNotFound,
    NotFound,
    UserNotFound,
)
from petisco.base.domain.errors.domain_error import DomainError
from petisco.base.domain.errors.unknown_error import UnknownError
from petisco.base.domain.message.all_message_subscriber import AllMessageSubscriber
from petisco.base.domain.message.command import Command
from petisco.base.domain.message.command_bus import CommandBus
from petisco.base.domain.message.command_subscriber import CommandSubscriber
from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.domain_event_bus import DomainEventBus
from petisco.base.domain.message.domain_event_subscriber import DomainEventSubscriber
from petisco.base.domain.message.file_domain_event_bus import FileDomainEventBus
from petisco.base.domain.message.message import Message
from petisco.base.domain.message.message_bus import MessageBus
from petisco.base.domain.message.message_consumer import MessageConsumer
from petisco.base.domain.message.message_subscriber import MessageSubscriber
from petisco.base.domain.message.not_implemented_command_bus import (
    NotImplementedCommandBus,
)
from petisco.base.domain.message.not_implemented_domain_event_bus import (
    NotImplementedDomainEventBus,
)
from petisco.base.domain.message.not_implemented_message_bus import (
    NotImplementedMessageBus,
)
from petisco.base.domain.message.not_implemented_message_comsumer import (
    NotImplementedMessageConsumer,
)
from petisco.base.domain.message.not_implemented_message_configurer import (
    NotImplementedMessageConfigurer,
)
from petisco.base.domain.model.aggregate_root import AggregateRoot
from petisco.base.domain.model.legacy_uuid import LegacyUuid
from petisco.base.domain.model.uuid import Uuid
from petisco.base.domain.model.value_object import ValueObject, ValueObjectSerializer
from petisco.base.domain.persistence.database import Database
from petisco.base.domain.persistence.databases import databases
from petisco.base.domain.value_objects.middleware_scope import MiddlewareScope
from petisco.base.misc.builder import Builder
from petisco.base.misc.datetime_serializer import DatetimeSerializer
from petisco.base.misc.interface import Interface
from petisco.base.misc.result_mapper import ResultMapper
from petisco.base.misc.singleton import Singleton
from petisco.base.misc.time_format import TIME_FORMAT
from petisco.base.testing.assert_http import assert_http

__all__ = [
    # base
    "Controller",
    "AsyncController",
    "unwrap_result_handler",
    "custom_message_handler",
    "ResultMapper",
    "Middleware",
    "MiddlewareScope",
    "NotifierMiddleware",
    "Notifier",
    "NotifierMessage",
    "NotifierExceptionMessage",
    "NotImplementedNotifier",
    "PrintMiddleware",
    "UseCase",
    "AsyncUseCase",
    "UseCaseUncontrolledError",
    "assert_http",
    "Dependency",
    "Container",
    "Message",
    "DomainEvent",
    "Command",
    "MessageBus",
    "NotImplementedMessageBus",
    "NotImplementedMessageConsumer",
    "NotImplementedMessageConfigurer",
    "DomainEventBus",
    "CommandBus",
    "FileDomainEventBus",
    "NotImplementedDomainEventBus",
    "NotImplementedCommandBus",
    "MessageSubscriber",
    "MessageConsumer",
    "AggregateRoot",
    "ValueObject",
    "ValueObjectSerializer",
    "DatetimeSerializer",
    "TIME_FORMAT",
    "Uuid",
    "LegacyUuid",
    "Interface",
    "DomainEventSubscriber",
    "CommandSubscriber",
    "AllMessageSubscriber",
    "databases",
    "Database",
    "Repository",
    "CrudRepository",
    "InmemoryCrudRepository",
    "AppService",
    "AsyncAppService",
    "Application",
    "ApplicationConfigurer",
    "Builder",
    "Singleton",
    # error
    "DEFAULT_HTTP_ERROR_MAP",
    "DomainError",
    "CriticalError",
    "NotFound",
    "AlreadyExists",
    "AggregateNotFoundError",
    "AggregatesNotFoundError",
    "AggregateAlreadyExistError",
    "UnknownError",
    "ClientNotFound",
    "ClientAlreadyExists",
    "UserNotFound",
    "UserAlreadyExists",
    "NotAllowed",
    "InvalidUuid",
    "InvalidValueObject",
    "HttpError",
    "ErrorMap",
    "BusCannotPublish",
]
