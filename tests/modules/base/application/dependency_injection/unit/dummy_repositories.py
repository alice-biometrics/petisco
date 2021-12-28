from abc import ABC, abstractmethod
from typing import List

from petisco import Container


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
        return MyRepoWithBuilderAndDependency(Container.get("repo"))

    def __init__(self, repository: Repo):
        self.repository = repository

    def execute(self):
        return self.repository.execute()


class MyRepoWithBuilderAndSeveralDependency(Repo):
    @staticmethod
    def build():
        return MyRepoWithBuilderAndSeveralDependency(
            [
                Container.get("repo-with-dependency"),
                Container.get("repo"),
                Container.get("other-repo"),
            ]
        )

    def __init__(self, repositories: List[Repo]):
        self.repositories = repositories

    def execute(self):
        for repo in self.repositories:
            repo.execute()


class InMemoryRepo(Repo):
    def execute(self):
        print("InMemoryRepo")
