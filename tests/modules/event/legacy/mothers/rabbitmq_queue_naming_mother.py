from tests.modules.event.mothers.defaults import DEFAULT_SERVICE


class RabbitMqQueueNamingMother:
    @staticmethod
    def main_queue():
        return f"{DEFAULT_SERVICE}-event"

    @staticmethod
    def dead_letter_queue():
        return f"dl-{RabbitMqQueueNamingMother.main_queue()}"
