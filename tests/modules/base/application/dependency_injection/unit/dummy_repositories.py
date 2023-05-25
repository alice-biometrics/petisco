from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from petisco import Container


class BaseRepo(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError


class OtherBaseRepo(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError


class MyRepo(BaseRepo):
    def execute(self):
        print("MyRepo")


T = TypeVar("T")


class MyGenericRepo(Generic[T], BaseRepo):
    def execute(self) -> T:
        print("MyRepo")


class MyOtherRepo(OtherBaseRepo):
    def execute(self):
        print("MyRepo")


class MyRepoWithBuilderAndDependency(BaseRepo):
    @staticmethod
    def build():
        return MyRepoWithBuilderAndDependency(Container.get("repo"))

    def __init__(self, repository: BaseRepo):
        self.repository = repository

    def execute(self):
        return self.repository.execute()


class MyRepoWithBuilderAndSeveralDependency(BaseRepo):
    @staticmethod
    def build():
        return MyRepoWithBuilderAndSeveralDependency(
            [
                Container.get("repo-with-dependency"),
                Container.get("repo"),
                Container.get("other-repo"),
            ]
        )

    def __init__(self, repositories: List[BaseRepo]):
        self.repositories = repositories

    def execute(self):
        for repo in self.repositories:
            repo.execute()


class InMemoryRepo(BaseRepo):
    def execute(self):
        print("InMemoryRepo")
