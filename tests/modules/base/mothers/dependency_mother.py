from typing import Any

from meiga import Result

from petisco import (
    Builder,
    Dependency,
    DomainEventBus,
    NotImplementedDomainEventBus,
    Repository,
)
from tests.modules.base.application.dependency_injection.unit.dummy_repositories import (
    BaseRepo,
)


class MyRepo(Repository):
    def save(self, *args: Any, **kwargs: Any) -> Result:
        pass

    def retrieve(self, *args: Any, **kwargs: Any) -> Result:
        pass

    def retrieve_all(self, *args: Any, **kwargs: Any) -> Result:
        pass

    def remove(self, *args: Any, **kwargs: Any) -> Result:
        pass


class DependencyMother:
    @staticmethod
    def any() -> Dependency:
        return Dependency(BaseRepo, builders={"default": Builder(MyRepo)})

    @staticmethod
    def legacy() -> Dependency:
        return Dependency(name="repo", builders={"default": Builder(MyRepo)})

    @staticmethod
    def domain_event_bus() -> Dependency:
        return Dependency(
            DomainEventBus, builders={"default": Builder(NotImplementedDomainEventBus)}
        )

    @staticmethod
    def create(name: str, builder: Any) -> Dependency:
        return Dependency(name=name, builders={"default": builder})
