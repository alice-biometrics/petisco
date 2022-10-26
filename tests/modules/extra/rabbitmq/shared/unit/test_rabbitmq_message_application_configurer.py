import pytest

from petisco import Builder, Container, Dependency, NotImplementedMessageConfigurer
from petisco.extra.rabbitmq import RabbitMqMessageApplicationConfigurer


@pytest.mark.unit
class TestRabbitMqMessageApplicationConfigurer:
    def setup_method(self):
        Container.set_dependencies(
            [
                Dependency(
                    name="message_configurer",
                    default_builder=Builder(
                        NotImplementedMessageConfigurer,
                    ),
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
        with pytest.raises(IndexError) as excinfo:
            configurer.execute()
        assert (
            "Invalid dependency. message_configurer is not found within available dependencies"
            in str(excinfo.value)
        )
