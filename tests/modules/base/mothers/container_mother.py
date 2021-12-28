from petisco import Container
from tests.modules.base.mothers.dependency_mother import DependencyMother


class ContainerMother:
    @staticmethod
    def any() -> Container:
        dependencies = [DependencyMother.any()]
        Container.set_dependencies(dependencies)
        return Container()
