from meiga import Failure

from petisco.base.domain.message.chaos.message_chaos_error import MessageChaosError
from petisco.extra.logger import DEBUG


def assert_logger_represents_simulated_failure_scenario(logger) -> None:
    def assert_redelivered_message(
        logging_message, expected_derived_action, check_headers: bool
    ) -> None:
        assert logging_message[0] == DEBUG
        assert logging_message[1]["meta"] == {
            "layer": "rabbitmq_message_consumer",
            "operation": "handle",
        }
        assert logging_message[1]["data"]["message"]["result"] == Failure(
            MessageChaosError()
        )
        derived_action = logging_message[1]["data"]["message"]["derived_action"]

        if check_headers:
            derived_action["headers"].pop("x-last-death-exchange")
            derived_action["headers"].pop("x-last-death-queue")
            derived_action["headers"].pop("x-last-death-reason")
            derived_action["headers"].pop("x-first-death-exchange")
            derived_action["headers"].pop("x-first-death-queue")
            derived_action["headers"].pop("x-first-death-reason")

        assert (
            derived_action == expected_derived_action
        ), f"{derived_action=} does not match with {expected_derived_action=}"

    def assert_send_to_retry(logging_message, redelivery_count, check_headers) -> None:
        expected_derived_action = {
            "action": "send_to_retry",
            "exchange_name": "retry.alice.petisco",
            "routing_key": "retry.alice.petisco.1.event.user_created.my_domain_event_subscriber",
            "headers": {
                "queue": "alice.petisco.1.event.user_created.my_domain_event_subscriber",
                "redelivery_count": redelivery_count,
            },
        }
        assert_redelivered_message(
            logging_message, expected_derived_action, check_headers
        )

    def assert_send_to_dead_leter(
        logging_message, redelivery_count, check_headers
    ) -> None:
        expected_derived_action = {
            "action": "send_to_dead_letter",
            "exchange_name": "dead_letter.alice.petisco",
            "routing_key": "dead_letter.alice.petisco.1.event.user_created.my_domain_event_subscriber",
            "headers": {
                "queue": "alice.petisco.1.event.user_created.my_domain_event_subscriber",
                "redelivery_count": redelivery_count,
            },
        }
        assert_redelivered_message(
            logging_message, expected_derived_action, check_headers
        )

    def assert_failure_simulator(logging_message) -> None:
        assert (
            logging_message[1]["data"]["message"]["chaos_action"] == "failure simulated"
        )

    # filter received_message logs
    logging_messages = [
        log_message
        for log_message in logger.get_logging_messages()
        if "log_activity" not in log_message[1]["data"]["message"]
        or log_message[1]["data"]["message"]["log_activity"] != "received_message"
    ]

    assert_send_to_retry(logging_messages[1], 1, False)

    redelivered_count = 2
    for i in range(3, 10, 2):
        assert_send_to_retry(logging_messages[i], redelivered_count, True)
        redelivered_count += 1

    for i in range(2, 10, 2):
        assert_failure_simulator(logging_messages[i])

    assert_send_to_dead_leter(logging_messages[-2], 6, True)
