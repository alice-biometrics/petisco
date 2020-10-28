from meiga import Result
from petisco.event.chaos.domain.interface_event_chaos import IEventChaos


class NotImplementedEventChaos(IEventChaos):
    def info(self):
        return {
            "EVENT_CHAOS_PERCENTAGE_SIMULATE_NACK": "NOT_IMPLEMENTED",
            "EVENT_CHAOS_DELAY_AFTER_OPERATION_SECONDS": "NOT_IMPLEMENTED",
            "EVENT_CHAOS_PERCENTAGE_SIMULATE_FAILURES": "NOT_IMPLEMENTED",
        }

    def nack_simulation(self, *args, **kwargs):
        pass

    def simulate_failure_on_result(self, result: Result) -> Result:
        return result

    def delay(self):
        pass
