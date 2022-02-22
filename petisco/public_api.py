# coding=utf-8
# Copyright (C) 2021+ Alice, Vigo, Spain

"""Public API of Alice Petisco Framework"""
from typing import List, Type

from petisco.base.application.application import Application
from petisco.base.application.application_configurer import ApplicationConfigurer
from petisco.base.application.controller.controller import Controller
from petisco.base.application.controller.http_error import HttpError
from petisco.base.application.dependency_injection.container import Container
from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.application.dependency_injection.injector import (  # deprecated
    Injector,
)
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
from petisco.base.application.patterns.crud_repository import CrudRepository
from petisco.base.application.patterns.inmemory_crud_repository import (
    InmemoryCrudRepository,
)
from petisco.base.application.patterns.repository import Repository
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
from petisco.base.domain.model.uuid import Uuid
from petisco.base.domain.model.value_object import ValueObject
from petisco.base.domain.persistence.persistence import Persistence
from petisco.base.domain.persistence.persistence_models import PersistenceModels
from petisco.base.misc.builder import Builder
from petisco.base.misc.interface import Interface
from petisco.base.misc.result_mapper import ResultMapper
from petisco.base.testing.assert_http import assert_http

base = [
    "Controller",
    "ResultMapper",
    "Middleware",
    "NotifierMiddleware",
    "Notifier",
    "NotifierMessage",
    "NotifierExceptionMessage",
    "NotImplementedNotifier",
    "PrintMiddleware",
    "UseCase",
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
    "NotImplementedDomainEventBus",
    "NotImplementedCommandBus",
    "MessageSubscriber",
    "MessageConsumer",
    "AggregateRoot",
    "ValueObject",
    "Uuid",
    "Interface",
    "DomainEventSubscriber",
    "CommandSubscriber",
    "AllMessageSubscriber",
    "Persistence",
    "PersistenceModels",
    "Repository",
    "CrudRepository",
    "InmemoryCrudRepository",
    "AppService",
    "Application",
    "ApplicationConfigurer",
    "Builder",
]

errors = [
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
]


deprecated = ["Injector"]
modules: List[str] = []

__all__ = base + errors + deprecated + modules
