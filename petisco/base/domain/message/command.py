from petisco.base.domain.message.message import Message


class Command(Message):
    def __init__(self, **kwargs):
        for k in kwargs:
            self.attributes[k] = kwargs[k]
            self.type = "command"
