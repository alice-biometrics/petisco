import uuid

EVENT_ID_LENGTH = 36


class EventId(str):
    def __init__(self, value):
        super(EventId, self).__init__()
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"{self.value}"

    @staticmethod
    def generate():
        return EventId(str(uuid.uuid4()))
