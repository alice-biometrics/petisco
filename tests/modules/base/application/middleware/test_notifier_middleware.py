from unittest.mock import patch

import pytest
from meiga import Failure, isSuccess

from petisco import CriticalError
from petisco.base.application.application_info import ApplicationInfo
from petisco.base.application.dependency_injection.container import Container
from petisco.base.application.middleware.notifier_middleware import NotifierMiddleware
from petisco.base.application.notifier.not_implemented_notifier import (
    NotImplementedNotifier,
)
from petisco.base.domain.errors.defaults.not_found import NotFound
from petisco.base.domain.errors.unknown_error import UnknownError
from petisco.base.misc.builder import Builder
from tests.modules.base.mothers.dependency_mother import DependencyMother


@pytest.mark.unit
class TestNotifierMiddleware:
    notifier_middleware: NotifierMiddleware

    def setup_method(self):
        notifier_dependency = DependencyMother.create(
            name="notifier", builder=Builder(NotImplementedNotifier)
        )
        Container.set_dependencies([notifier_dependency])

        self.notifier_middleware = NotifierMiddleware(
            wrapped_class_name="class_name", wrapped_class_input_arguments=()
        )

    def teardown_method(self):
        Container.clear()
        ApplicationInfo.clear()

    @patch.object(NotImplementedNotifier, "publish_exception")
    def should_not_notify_success_results(self, mock_notifier):
        self.notifier_middleware.after(result=isSuccess)
        mock_notifier.assert_not_called()

    @patch.object(NotImplementedNotifier, "publish_exception")
    def should_not_notify_domain_error_failure_results(self, mock_notifier):
        self.notifier_middleware.after(result=Failure(NotFound()))
        mock_notifier.assert_not_called()

    @patch.object(NotImplementedNotifier, "publish_exception")
    def should_notify_unknown_error_failure_results(self, mock_notifier):
        self.notifier_middleware.after(
            result=Failure(UnknownError(exception=TypeError()))
        )
        mock_notifier.assert_called()

    @patch.object(NotImplementedNotifier, "publish_exception")
    def should_notify_unknown_error_failure_results_with_meta_information(
        self, mock_notifier
    ):
        ApplicationInfo(name="app_name", version="app_version")
        self.notifier_middleware.after(
            result=Failure(UnknownError(exception=TypeError()))
        )

        mock_notifier.assert_called()
        exception_message = mock_notifier.call_args[0][0]
        assert exception_message.meta["application_name"] == "app_name"
        assert exception_message.meta["application_version"] == "app_version"

    @patch.object(NotImplementedNotifier, "publish")
    def should_notify_critical_error_failure_results_with_meta_information(
        self, mock_notifier
    ):
        ApplicationInfo(name="app_name", version="app_version")
        self.notifier_middleware.after(result=Failure(CriticalError()))

        mock_notifier.assert_called()
        exception_message = mock_notifier.call_args[0][0]
        assert exception_message.meta["application_name"] == "app_name"
        assert exception_message.meta["application_version"] == "app_version"
