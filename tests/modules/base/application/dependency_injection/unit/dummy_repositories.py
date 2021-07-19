from abc import ABC, abstractmethod


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
