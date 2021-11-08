from petisco import NotifierMessage


class NotifierMessageMother:
    @staticmethod
    def any() -> NotifierMessage:
        return NotifierMessage(title="test title", message="test message")
