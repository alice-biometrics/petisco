from typing import Any

from meiga import AnyResult

from petisco import __version__
from petisco.base.application.application_info import ApplicationInfo
from petisco.base.application.dependency_injection.container import Container
from petisco.base.application.middleware.middleware import Middleware
from petisco.base.application.notifier.notifier_exception_message import (
    NotifierExceptionMessage,
)
from petisco.base.application.notifier.notifier_message import NotifierMessage
from petisco.base.domain.errors.critical_error import CriticalError
from petisco.base.domain.errors.unknown_error import UnknownError


class NotifierMiddleware(Middleware):
    """
    Middleware Implementation to notify critical and unknown errors.

    This Middleware will check result and notify if necessary using Container.get("notifier") set dependency.
    """

    def __init__(
        self, wrapped_class_name: str, wrapped_class_input_arguments: Any
    ) -> None:
        super().__init__(wrapped_class_name, wrapped_class_input_arguments)
        self.notifier = Container.get("notifier")

    def before(self) -> None:
        pass

    def after(self, result: AnyResult) -> None:
        if result.is_failure:
            error = result.value

            meta = {
                "petisco": __version__,
                "application_name": ApplicationInfo().name,
                "application_version": ApplicationInfo().version,
            }
            if issubclass(error.__class__, UnknownError):
                notifier_exception_message = (
                    NotifierExceptionMessage.from_unknown_error(
                        error, title="Uncontrolled Exception"
                    )
                )
                notifier_exception_message.update_meta(meta)
                self.notifier.publish_exception(notifier_exception_message)
            if issubclass(error.__class__, CriticalError):
                notifier_message = NotifierMessage(
                    title=error.get_specify_detail(),
                    message=error.__repr__(),
                    meta=meta,
                )
                self.notifier.publish(notifier_message)
