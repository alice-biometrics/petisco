from petisco.application.singleton import Singleton


class SqlAlchemyPersistence(metaclass=Singleton):
    @staticmethod
    def get_instance():
        return SqlAlchemyPersistence()

    def __init__(self, session=None, base=None):
        self.session = session
        self.base = base
