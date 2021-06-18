from petisco.base.domain.message.message import Message


class DomainEvent(Message):
    def __init__(self, **kwargs):
        for k in kwargs:
            self.attributes[k] = kwargs[k]
            self.type = "domain_event"
