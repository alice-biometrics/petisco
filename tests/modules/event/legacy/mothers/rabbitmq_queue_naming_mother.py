from tests.modules.event.mothers.defaults import DEFAULT_SERVICE


class RabbitMqQueueNamingMother:
    @staticmethod
    def legacy_main_queue():
        return f"{DEFAULT_SERVICE}-event"

    @staticmethod
    def legacy_dead_letter_queue():
        return f"dl-{RabbitMqQueueNamingMother.legacy_main_queue()}"
