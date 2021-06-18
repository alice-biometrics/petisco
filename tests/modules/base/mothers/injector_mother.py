from petisco import Injector, Dependency


class MyRepo:
    def execute(self):
        print("MyRepo")


class InjectorMother:
    @staticmethod
    def any() -> Injector:
        dependencies = [Dependency(name="repo", default_instance=MyRepo())]
        return Injector(dependencies)
