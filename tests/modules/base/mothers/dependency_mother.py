from typing import List

from meiga import Result

from petisco import Builder, Dependency, NotImplementedMessageBusBuilder, Repository


class MyRepo(Repository):
    def save(self, *args, **kwargs) -> Result:
        pass

    def retrieve(self, *args, **kwargs) -> Result:
        pass

    def retrieve_all(self, *args, **kwargs) -> Result:
        pass

    def remove(self, *args, **kwargs) -> Result:
        pass


class MyRepoBuilder(Builder):
    def build(self):
        return MyRepo()


class DependencyMother:
    @staticmethod
    def any() -> Dependency:
        return Dependency(name="repo", default_builder=MyRepoBuilder())

    @staticmethod
    def several() -> List[Dependency]:
        return [
            Dependency(name="repo", default_builder=MyRepoBuilder()),
            # Dependency(name="app_service", default_instance=MyRepo())
        ]

    @staticmethod
    def domain_event_bus() -> Dependency:
        return Dependency(
            name="domain_event_bus", default_builder=NotImplementedMessageBusBuilder()
        )
