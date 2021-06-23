from petisco.base.domain.message.chaos.message_chaos import MessageChaos


class NotImplementedMessageChaos(MessageChaos):
    def info(self):
        return {
            "EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK": "NOT_IMPLEMENTED",
            "EVENT_CHAOS_DELAY_AFTER_OPERATION_SECONDS": "NOT_IMPLEMENTED",
            "EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES": "NOT_IMPLEMENTED",
        }

    def nack_simulation(self, *args, **kwargs) -> bool:
        return False

    def failure_simulation(self, *args, **kwargs) -> bool:
        return False

    def delay(self):
        pass
