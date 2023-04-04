import pytest

from petisco import Builder, Container, Dependency, NotImplementedMessageConfigurer
from petisco.base.domain.message.message_configurer import MessageConfigurer
from petisco.extra.rabbitmq import RabbitMqMessageApplicationConfigurer


@pytest.mark.unit
class TestRabbitMqMessageApplicationConfigurer:
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
                )
            ]
        )

    def teardown_method(self):
        Container.clear()

    @pytest.mark.parametrize("testing", [True, False])
    def should_execute(self, testing):
        configurer = RabbitMqMessageApplicationConfigurer()
        configurer.execute(testing=testing)

    def should_fail_when_message_configurer_do_not_exist_in_container(self):
        Container.clear()
        configurer = RabbitMqMessageApplicationConfigurer()
        with pytest.raises(IndexError, match="Invalid dependency."):
            configurer.execute()
