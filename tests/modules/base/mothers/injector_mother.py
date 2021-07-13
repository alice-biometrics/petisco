from petisco import Injector
from tests.modules.base.mothers.dependency_mother import DependencyMother


class InjectorMother:
    @staticmethod
    def any() -> Injector:
        dependencies = [DependencyMother.any()]
        return Injector(dependencies)
