from petisco import Uuid


class UuidMother:
    @staticmethod
    def any() -> Uuid:
        return Uuid("7b6ef019-02d7-410e-bd85-7b3104423608")

    @staticmethod
    def secondary() -> Uuid:
        return Uuid("0c4b86a7-662f-4ab0-a566-101d0aee34a9")

    @staticmethod
    def random() -> Uuid:
        return Uuid.v4()
