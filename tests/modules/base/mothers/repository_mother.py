from meiga import Result

from petisco.base.application.repository.interface_repository import Repository


class MyRepository(Repository):
    def save(self, *args, **kwargs) -> Result:
        pass

    def retrieve(self, *args, **kwargs) -> Result:
        pass

    def retrieve_all(self, *args, **kwargs) -> Result:
        pass

    def remove(self, *args, **kwargs) -> Result:
        pass


class RepositoryMother:
    @staticmethod
    def valid() -> Repository:
        return MyRepository()
