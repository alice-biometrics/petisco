from abc import ABC, abstractmethod

from petisco import Builder


class Repo(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError


class MyRepo(Repo):
    def execute(self):
        print("MyRepo")


class InMemoryRepo(Repo):
    def execute(self):
        print("InMemoryRepo")


class MyRepoBuilder(Builder):
    def build(self) -> MyRepo:
        return MyRepo()


class InMemoryRepoBuilder(Builder):
    def build(self) -> InMemoryRepo:
        return InMemoryRepo()
