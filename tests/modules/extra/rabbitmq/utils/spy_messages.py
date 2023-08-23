from petisco import Message, Uuid


class SpyMessages:
    def __init__(self) -> None:
        self.counter_messages = {}
        self.messages = []

    def __repr__(self) -> str:
        return f"SpyMessages: {self.messages}"

    def append(self, message: Message) -> None:
        self.messages.append(message)
        if str(message.get_message_id()) not in self.counter_messages:
            self.counter_messages[str(message.get_message_id())] = {"counter": 1}
        else:
            self.counter_messages[str(message.get_message_id())]["counter"] += 1

    def assert_number_total_messages(self, expected_number_messages: int) -> None:
        actual_number_total_messages = len(self.messages)
        assert (
            expected_number_messages == actual_number_total_messages
        ), f"Expected total messages is {expected_number_messages}, actual {actual_number_total_messages}. [{self.counter_messages}]"

    def assert_number_unique_messages(self, expected_number_messages: int) -> None:
        actual_number_messages = len(self.counter_messages.keys())
        assert (
            actual_number_messages == expected_number_messages
        ), f"Expected number of unique messages is {expected_number_messages}, actual {actual_number_messages}. [{self.counter_messages}]"

    def get_counter_by_message_id(self, message_id: Uuid) -> int:
        return self.counter_messages.get(str(message_id), {}).get("counter", 0)

    def assert_count_by_message_id(self, message_id: Uuid, expected_count: int) -> None:
        assert (
            self.get_counter_by_message_id(message_id) == expected_count
        ), f"Expected events is {expected_count}, actual {self.get_counter_by_message_id(message_id)}. [{self.counter_messages}]"

    def assert_first_message(self, expected_message: Message) -> None:
        self.assert_number_unique_messages(1)
        event = self.messages[0]
        assert event == expected_message

    def assert_last_message(self, expected_message: Message) -> None:
        self.assert_number_unique_messages(1)
        event = self.messages[-1]
        assert event == expected_message
