from typing import Any

from meiga import Result

from petisco.base.application.patterns.repository import Repository


class MyRepository(Repository):
    def save(self, *args: Any, **kwargs: Any) -> Result:
        pass

    def retrieve(self, *args: Any, **kwargs: Any) -> Result:
        pass

    def retrieve_all(self, *args: Any, **kwargs: Any) -> Result:
        pass

    def remove(self, *args: Any, **kwargs: Any) -> Result:
        pass


class RepositoryMother:
    @staticmethod
    def valid() -> Repository:
        return MyRepository()
