# coding=utf-8
# Copyright (C) 2019+ Alice, Vigo, Spain

"""Public API of ALiCE Petisco Framework"""


# Classes
from petisco.application.application_config import ApplicationConfig
from petisco.application.repository import Repository
from petisco.application.service import Service
from petisco.logger.logging_based_logger import LoggingBasedLogger
from petisco.logger.logger import Logger
from petisco.use_case import UseCase
from petisco.use_case import use_case_logger
from petisco.controller.controller_decorator import controller
from petisco.controller.correlation_id import CorrelationId
from petisco.controller.errors.http_error import HttpError

classes = [
    "ApplicationConfig",
    "Service",
    "Repository",
    "UseCase",
    "use_case_logger",
    "controller",
    "CorrelationId",
    "HttpError",
    "LoggingBasedLogger",
    "Logger",
]

# Constants
from petisco.logger.logger import (
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
    flask = ""

__all__ = classes + constants + flask
