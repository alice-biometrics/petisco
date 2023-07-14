import pytest

from petisco import (
    Builder,
    Container,
    Dependency,
    MessageConsumer,
    NotImplementedMessageConfigurer,
    NotImplementedMessageConsumer,
)
from petisco.base.domain.message.message_configurer import MessageConfigurer
from petisco.extra.rabbitmq import RabbitMqConfigurer


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
        configurer_alias = "message_configurer_alias"
        consumer_alias = "message_consumer_alias"
        Container.clear()
        Container.set_dependencies(
            [
                Dependency(
                    MessageConfigurer,
                    alias=configurer_alias,
                    builders={"default": Builder(NotImplementedMessageConfigurer)},
                ),
                Dependency(
                    MessageConsumer,
                    alias=consumer_alias,
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
            configurer_alias=configurer_alias,
            consumer_alias=consumer_alias,
        )
        configurer.execute(testing=testing)

    def should_fail_when_message_dependencies_do_not_exist_in_container_with_alias(
        self,
    ):
        configurer_alias = "message_configurer_alias"
        consumer_alias = "message_consumer_alias"
        configurer = RabbitMqConfigurer(
            subscribers=self.subscribers,
            configurer_alias=configurer_alias,
            consumer_alias=consumer_alias,
        )
        with pytest.raises(IndexError, match="Invalid dependency."):
            configurer.execute()

    def should_fail_when_message_dependencies_do_not_exist_in_container(self):
        Container.clear()
        configurer = RabbitMqConfigurer(subscribers=self.subscribers)
        with pytest.raises(IndexError, match="Invalid dependency."):
            configurer.execute()
