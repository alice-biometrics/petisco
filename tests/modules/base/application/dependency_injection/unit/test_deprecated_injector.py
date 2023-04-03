import pytest

from petisco import Builder, Dependency, Injector
from tests.modules.base.application.dependency_injection.unit.dummy_repositories import (
    BaseRepo,
    InMemoryRepo,
    MyRepo,
    MyRepoWithBuilderAndDependency,
    MyRepoWithBuilderAndSeveralDependency,
)


@pytest.mark.unit
class TestDeprecatedInjector:
    def should_success_when_access_one_dynamic_attr_representing_a_dependency(self):
        dependencies = [Dependency(name="repo", default_builder=Builder(MyRepo))]

        Injector.set_dependencies(dependencies)

        assert Injector.get_available_dependencies() == ["repo"]

        assert isinstance(Injector().get("repo"), MyRepo)

        Injector.clear()

    @pytest.mark.parametrize(
        "dependencies,expected_available_dependencies",
        [
            ([], []),
            ([Dependency(name="repo", default_builder=Builder(MyRepo))], ["repo"]),
            (
                [
                    Dependency(name="repo", default_builder=Builder(MyRepo)),
                    Dependency(
                        name="inmemory_repo", default_builder=Builder(InMemoryRepo)
                    ),
                ],
                ["repo", "inmemory_repo"],
            ),
        ],
    )
    def should_return_several_available_dependencies(
        self, dependencies, expected_available_dependencies
    ):

        Injector.set_dependencies(dependencies)

        assert Injector.get_available_dependencies() == expected_available_dependencies

        Injector.clear()

    @pytest.mark.parametrize(
        "dependencies",
        [
            [
                Dependency(
                    name="repo-with-dependency",
                    default_builder=Builder(
                        MyRepoWithBuilderAndDependency, is_builder=True
                    ),
                ),
                Dependency(name="repo", default_builder=Builder(MyRepo)),
            ],
            [
                Dependency(name="repo", default_builder=Builder(MyRepo)),
                Dependency(
                    name="repo-with-dependency",
                    default_builder=Builder(
                        MyRepoWithBuilderAndDependency, is_builder=True
                    ),
                ),
            ],
            [
                Dependency(name="repo", default_builder=Builder(MyRepo)),
                Dependency(name="other-repo", default_builder=Builder(MyRepo)),
                Dependency(
                    name="repo-with-dependency",
                    default_builder=Builder(
                        MyRepoWithBuilderAndDependency, is_builder=True
                    ),
                ),
                Dependency(
                    name="repo-with-3-dependencies",
                    default_builder=Builder(
                        MyRepoWithBuilderAndSeveralDependency, is_builder=True
                    ),
                ),
            ],
        ],
    )
    def should_success_when_add_dependecies_which_depends_from_another_dependency(
        self,
        dependencies,
    ):
        expected_dependencies_names = [dependency.name for dependency in dependencies]

        Injector.set_dependencies(dependencies)

        assert (
            Injector.get_available_dependencies().sort()
            == expected_dependencies_names.sort()
        )

        for name in expected_dependencies_names:
            assert isinstance(Injector().get(name), BaseRepo)

        Injector.clear()
