from abc import ABC, abstractmethod

from petisco import Injector


class Repo(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError


class MyRepo(Repo):
    def execute(self):
        print("MyRepo")


class MyRepoWithBuilderAndDependency(Repo):
    @staticmethod
    def build():
        return MyRepoWithBuilderAndDependency(Injector.get("repo"))

    def __init__(self, repository: Repo):
        self.repository = repository

    def execute(self):
        return self.repository.execute()


class InMemoryRepo(Repo):
    def execute(self):
        print("InMemoryRepo")
