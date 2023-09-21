from petisco import Message


class MessageMother:
    @staticmethod
    def any() -> Message:
        return Message()

    @staticmethod
    def other(message_name: str = "other") -> Message:
        message = Message()
        message._message_name = message_name
        return message
