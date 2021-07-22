from meiga import Result

from petisco import __version__
from petisco.base.application.dependency_injection.injector import Injector
from petisco.base.application.middleware.middleware import Middleware
from petisco.base.application.notifier.notifier_exception_message import (
    NotifierExceptionMessage,
)
from petisco.base.domain.errors.unknown_error import UnknownError


class NotifierMiddleware(Middleware):
    def __init__(self, wrapped_class_name, wrapped_class_input_arguments):
        super().__init__(wrapped_class_name, wrapped_class_input_arguments)
        self.notifier = Injector.get("notifier")

    def before(self):
        pass

    def after(self, result: Result):
        if result.is_failure:
            error = result.value
            if issubclass(error.__class__, UnknownError):
                notifier_exception_message = (
                    NotifierExceptionMessage.from_unknown_error(
                        error, title="Uncontrolled Exception"
                    )
                )
                notifier_exception_message.meta["petisco"] = __version__
                self.notifier.publish_exception(notifier_exception_message)
