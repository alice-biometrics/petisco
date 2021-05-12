from meiga import Result
from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.domain.errors.critical_error import CriticalError
from petisco.notifier.domain.interface_notifier import INotifier
from petisco.notifier.domain.notifier_exception_message import NotifierExceptionMessage
from petisco.notifier.infrastructure.not_implemented_notifier import (
    NotImplementedNotifier,
)
from petisco.v1.middleware.middleware import Middleware


class NotifierMiddleware(Middleware):
    def __init__(self, info_id: InfoId, notifier: INotifier):
        self.info_id = info_id
        self.notifier = notifier

    def before(self):
        pass

    def after(self, result: Result):
        if result.is_failure:
            error = result.value
            if issubclass(error.__class__, CriticalError):
                self.notifier.publish(
                    NotifierExceptionMessage(
                        exception=error.exception,
                        executor=error.executor,
                        input_parameters=error.input_parameters,
                        traceback=error.traceback,
                        info_id=self.info_id,
                        info_petisco={},  # Petisco.get_info(),
                    )
                )


class NotifierMiddlewareBuilder:
    @staticmethod
    def not_implemented(info_id: InfoId):
        return NotifierMiddleware(info_id=info_id, notifier=NotImplementedNotifier())
