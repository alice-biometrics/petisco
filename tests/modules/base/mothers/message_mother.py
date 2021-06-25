from petisco import Message


class MessageMother:
    @staticmethod
    def any() -> Message:
        return Message()
