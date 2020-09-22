from petisco.application.singleton import Singleton


class SqlAlchemyPersistence(metaclass=Singleton):
    @staticmethod
    def get_instance():
        return SqlAlchemyPersistence()

    def __init__(self):
        self.sources = {}
