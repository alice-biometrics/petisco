import pytest

from petisco import Builder, Container, Dependency
from tests.modules.base.application.dependency_injection.unit.dummy_repositories import (
    BaseRepo,
    InMemoryRepo,
    MyRepo,
    MyRepoWithBuilderAndDependency,
    MyRepoWithBuilderAndSeveralDependency,
)


@pytest.mark.unit
class TestDeprecatedContainer:
    def should_success_when_access_one_dynamic_attr_representing_a_dependency(self):
        dependencies = [Dependency(name="repo", default_builder=Builder(MyRepo))]

        Container.set_dependencies(dependencies)

        assert Container.get_available_dependencies() == ["repo"]

        assert isinstance(Container.get("repo"), MyRepo)

        Container.clear()

    def should_success_when_access_one_dynamic_attr_representing_a_dependency_with_alias_deprecated_name(
        self,
    ):
        dependencies = [
            Dependency(BaseRepo, name="my-alias", default_builder=Builder(MyRepo))
        ]

        Container.set_dependencies(dependencies)

        assert Container.get_available_dependencies() == ["my-alias"]

        with pytest.raises(IndexError, match="Invalid dependency"):
            Container.get(BaseRepo)

        instance = Container.get("my-alias")

        assert isinstance(instance, MyRepo)

        Container.clear()

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

        Container.set_dependencies(dependencies)

        assert Container.get_available_dependencies() == expected_available_dependencies

        Container.clear()

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
    def should_success_when_add_dependencies_which_depends_from_another_dependency(
        self,
        dependencies,
    ):
        expected_dependencies_names = [dependency.name for dependency in dependencies]

        Container.set_dependencies(dependencies)

        assert (
            Container.get_available_dependencies().sort()
            == expected_dependencies_names.sort()
        )

        for name in expected_dependencies_names:
            assert isinstance(Container().get(name), BaseRepo)

        Container.clear()

    @pytest.mark.parametrize(
        "dependencies",
        [
            (
                [
                    Dependency[BaseRepo](
                        name="my-alias", default_builder=Builder(MyRepo)
                    ),
                    Dependency[BaseRepo](
                        name="my-alias", default_builder=Builder(MyRepo)
                    ),
                ]
            ),
            (
                [
                    Dependency(name="my-alias", default_builder=Builder(MyRepo)),
                    Dependency(name="my-alias", default_builder=Builder(MyRepo)),
                ]
            ),
        ],
    )
    def should_raise_exception_if_there_is_duplicated_dependencies(self, dependencies):
        with pytest.raises(IndexError):
            Container.set_dependencies(dependencies, overwrite=False)

        Container.clear()
