from unittest.mock import patch

import pytest

from petisco import (
    Builder,
    Container,
    Dependency,
    MessageConsumer,
    NotImplementedMessageConfigurer,
    NotImplementedMessageConsumer,
    NotImplementedNotifier,
)
from petisco.base.domain.message.message_configurer import MessageConfigurer
from petisco.extra.rabbitmq import RabbitMqConfigurer
from petisco.extra.slack import get_default_notifier_dependencies


@pytest.mark.unit
class TestRabbitMqConfigurer:
    def setup_method(self):
        Container.set_dependencies(
            [
                Dependency(
                    MessageConfigurer,
                    builders={
                        "default": Builder(
                            NotImplementedMessageConfigurer,
                        )
                    },
                ),
                Dependency(
                    MessageConsumer,
                    builders={
                        "default": Builder(
                            NotImplementedMessageConsumer,
                        )
                    },
                ),
            ]
            + get_default_notifier_dependencies()
        )
        self.subscribers = []

    def teardown_method(self):
        Container.clear()

    @pytest.mark.parametrize(
        "start_consuming,testing",
        [(True, True), (True, False), (False, True), (False, False)],
    )
    def should_execute(self, start_consuming, testing):
        configurer = RabbitMqConfigurer(
            subscribers=self.subscribers, start_consuming=start_consuming
        )
        configurer.execute(testing=testing)

    @pytest.mark.parametrize(
        "start_consuming,testing",
        [(True, True), (True, False), (False, True), (False, False)],
    )
    def should_execute_with_dependencies_with_alias(self, start_consuming, testing):
        alias = "other"
        Container.clear()
        Container.set_dependencies(
            [
                Dependency(
                    MessageConfigurer,
                    alias=alias,
                    builders={"default": Builder(NotImplementedMessageConfigurer)},
                ),
                Dependency(
                    MessageConsumer,
                    alias=alias,
                    builders={
                        "default": Builder(
                            NotImplementedMessageConsumer,
                        )
                    },
                ),
            ]
        )
        configurer = RabbitMqConfigurer(
            subscribers=self.subscribers,
            start_consuming=start_consuming,
            alias=alias,
        )
        configurer.execute(testing=testing)

    def should_fail_when_message_dependencies_do_not_exist_in_container_with_alias(
        self,
    ):
        alias = "other"
        configurer = RabbitMqConfigurer(
            subscribers=self.subscribers,
            alias=alias,
        )
        with pytest.raises(IndexError, match="Invalid dependency."):
            configurer.execute()

    def should_fail_when_message_dependencies_do_not_exist_in_container(self):
        Container.clear()
        configurer = RabbitMqConfigurer(subscribers=self.subscribers)
        with pytest.raises(IndexError, match="Invalid dependency."):
            configurer.execute()

    def should_notify_and_not_fail_when_there_is_a_connection_error(self):
        configurer = RabbitMqConfigurer(subscribers=self.subscribers)
        with patch.object(
            NotImplementedMessageConfigurer,
            "configure_subscribers",
            side_effect=ConnectionError(),
        ) as mock_message_configurer:
            with patch.object(
                NotImplementedNotifier, "publish_exception"
            ) as notifier_mock:
                configurer.execute()
        mock_message_configurer.assert_called_once()
        notifier_mock.assert_called_once()
