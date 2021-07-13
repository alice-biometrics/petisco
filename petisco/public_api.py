# coding=utf-8
# Copyright (C) 2019+ Alice, Vigo, Spain

"""Public API of ALiCE Petisco Framework"""
from petisco.base.application.application import Application
from petisco.base.application.controller.controller import Controller
from petisco.base.application.controller.http_error import HttpError
from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.application.dependency_injection.injector import Injector
from petisco.base.application.middleware.middleware import Middleware
from petisco.base.application.middleware.notifier_middleware import NotifierMiddleware
from petisco.base.application.middleware.print_middleware import PrintMiddleware
from petisco.base.application.repository.interface_repository import Repository
from petisco.base.application.repository.repositories import Repositories
from petisco.base.application.use_case.use_case import UseCase
from petisco.base.application.use_case.use_case_uncontrolled_error import (
    UseCaseUncontrolledError,
)
from petisco.base.domain.errors.default_http_error_map import DEFAULT_HTTP_ERROR_MAP
from petisco.base.domain.errors.defaults.already_exists import (
    AlreadyExists,
    ClientAlreadyExists,
    UserAlreadyExists,
)
from petisco.base.domain.errors.defaults.invalid_uuid import InvalidUuid
from petisco.base.domain.errors.defaults.invalid_value_object import InvalidValueObject
from petisco.base.domain.errors.defaults.not_allowed import NotAllowed
from petisco.base.domain.errors.defaults.not_found import (
    ClientNotFound,
    NotFound,
    UserNotFound,
)
from petisco.base.domain.errors.domain_error import DomainError
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
from petisco.base.domain.message.not_implemented_domain_event_bus import (
    NotImplementedDomainEventBus,
)
from petisco.base.domain.message.not_implemented_message_bus import (
    NotImplementedMessageBus,
)
from petisco.base.domain.model.aggregate_root import AggregateRoot
from petisco.base.domain.model.uuid import Uuid
from petisco.base.domain.model.value_object import ValueObject
from petisco.base.domain.persistence.persistence import Persistence
from petisco.base.domain.persistence.persistence_models import PersistenceModels

# TODO permit use from petisco.fastapi import *
# from petisco.extra import fastapi
from petisco.base.misc.interface import Interface
from petisco.base.misc.result_mapper import ResultMapper
from petisco.base.testing.assert_http import assert_http

base = [
    "Controller",
    "ResultMapper",
    "Middleware",
    "NotifierMiddleware",
    "PrintMiddleware",
    "UseCase",
    "UseCaseUncontrolledError",
    "DEFAULT_HTTP_ERROR_MAP",
    "assert_http",
    "DomainError",
    "NotFound",
    "AlreadyExists",
    "ClientNotFound",
    "ClientAlreadyExists",
    "UserNotFound",
    "UserAlreadyExists",
    "NotAllowed",
    "InvalidUuid",
    "Dependency",
    "Injector",
    "Message",
    "DomainEvent",
    "Command",
    "MessageBus",
    "NotImplementedMessageBus",
    "DomainEventBus",
    "CommandBus",
    "NotImplementedDomainEventBus",
    "MessageSubscriber",
    "MessageConsumer",
    "AggregateRoot",
    "ValueObject",
    "Uuid",
    "HttpError",
    "Interface",
    "DomainEventSubscriber",
    "CommandSubscriber",
    "AllMessageSubscriber",
    "Persistence",
    "PersistenceModels",
    "InvalidValueObject",
    "Repositories",
    "Repository",
    "Application",
]
modules = []  # ["extra.fastapi"]


__all__ = base + modules
