import inspect
from typing import Dict, TypeVar, Callable

from deprecation import deprecated

from petisco.application.singleton import Singleton
from petisco.application.interface_repository import IRepository

Repository = TypeVar("Repository", bound=IRepository)


class Repositories(metaclass=Singleton):
    def __init__(self, repositories: Dict[str, Repository] = None):
        self._repositories = repositories if repositories else {}

    def get_info(self):
        return {
            name: repository.info() for name, repository in self._repositories.items()
        }

    @staticmethod
    def info():
        return Repositories.get_instance().get_info()

    @staticmethod
    def load(provider: Callable):
        repositories = provider()
        return Repositories(repositories)

    @staticmethod
    def get_instance():
        try:
            return Repositories()
        except Exception as e:  # noqa E722
            frame_info = inspect.stack()[1]
            raise ImportError(
                f"Repositories must be configured. If not, you cannot obtain repositories\n"
                f"Following code must be executed after Repositories initialization:\n"
                f"\tfilename: {frame_info.filename}\n"
                f"\tlineno: {frame_info.lineno}\n"
                f"\tfunction: {frame_info.function}\n"
                f"\tcode_context: {frame_info.code_context}\n\n"
            )

    def add(self, name: str, repository: Repository):
        if name in self._repositories:
            raise NameError(f"Repository {name} is already added to Repositories")
        self._repositories[name] = repository

    def remove(self, name: str):
        if name in self._repositories:
            del self._repositories[name]
        else:
            raise IndexError(f"Repository cannot be removed. {name} not exists")

    @staticmethod
    def get(name: str) -> Repository:
        repositories = Repositories.get_instance()._repositories
        if repositories is None:
            raise ValueError(
                "Repositories: no repository has been declared. Please, initialize it (i.e Repositories.from_provider(provider_func))"
            )
        repository = repositories.get(name)
        if not repository:
            raise ValueError(
                f"Repositories: {name} repository is not defined.  Please, add it (i.e Repositories.from_provider(provider_func))"
            )
        return repository

    @staticmethod
    @deprecated("This method is deprecated. Please, use Repositories.load")
    def from_provider(provider: Callable):
        return Repositories.load(provider)
