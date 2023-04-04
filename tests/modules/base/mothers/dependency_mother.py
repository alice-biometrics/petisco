from typing import Any, List

from meiga import Result

from petisco import (
    Builder,
    Dependency,
    DomainEventBus,
    NotImplementedDomainEventBus,
    Repository,
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
        return Dependency(name="repo", builders={"default": Builder(MyRepo)})

    @staticmethod
    def several() -> List[Dependency]:
        return [
            Dependency(name="repo", builders={"default": Builder(MyRepo)}),
            # Dependency(name="app_service", default_instance=MyRepo())
        ]

    @staticmethod
    def domain_event_bus() -> Dependency:
        return Dependency(
            DomainEventBus, builders={"default": Builder(NotImplementedDomainEventBus)}
        )

    @staticmethod
    def create(name: str, builder: Any) -> Dependency:
        return Dependency(name=name, builders={"default": builder})
