from petisco import NotifierExceptionMessage


class NotifierExceptionMessageMother:
    @staticmethod
    def any() -> NotifierExceptionMessage:
        return NotifierExceptionMessage(
            title="test title",
            executor="test executor",
            exception=TypeError(),
            traceback="traceback",
        )

    @staticmethod
    def long() -> NotifierExceptionMessage:
        return NotifierExceptionMessage(
            title="test title",
            executor="test executor" * 50,
            exception=TypeError(),
            traceback="traceback" * 9999,
        )
