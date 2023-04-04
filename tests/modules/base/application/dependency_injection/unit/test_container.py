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
class TestContainer:
    def should_success_when_access_one_dynamic_attr_representing_a_dependency_with_type(
        self,
    ):
        dependencies = [Dependency(BaseRepo, builders={"default": Builder(MyRepo)})]

        Container.set_dependencies(dependencies)

        assert Container.get_available_dependencies() == [BaseRepo.__name__]

        instance = Container.get(BaseRepo)

        assert isinstance(instance, MyRepo)

        Container.clear()

    def should_success_when_access_one_dynamic_attr_representing_a_dependency_with_alias(
        self,
    ):
        dependencies = [
            Dependency(
                BaseRepo, alias="my-alias", builders={"default": Builder(MyRepo)}
            )
        ]

        Container.set_dependencies(dependencies)

        assert Container.get_available_dependencies() == ["my-alias"]

        with pytest.raises(IndexError, match="Invalid dependency"):
            Container.get(BaseRepo)

        instance = Container.get(MyRepo, alias="my-alias")

        assert isinstance(instance, MyRepo)

        Container.clear()

    def should_success_when_define_two_dependencies_with_the_same_base_type(self):
        dependencies = [
            Dependency(BaseRepo, builders={"default": Builder(MyRepo)}),
            Dependency(
                BaseRepo, alias="my-alias", builders={"default": Builder(MyRepo)}
            ),
        ]

        Container.set_dependencies(dependencies)

        assert Container.get_available_dependencies() == ["BaseRepo", "my-alias"]

        instance_base_type = Container.get(BaseRepo)
        instance_with_alias = Container.get(BaseRepo, alias="my-alias")

        assert isinstance(instance_base_type, MyRepo)
        assert isinstance(instance_with_alias, MyRepo)

        Container.clear()

    @pytest.mark.parametrize(
        "dependencies",
        [
            (
                [
                    Dependency(BaseRepo, builders={"default": Builder(MyRepo)}),
                    Dependency(BaseRepo, builders={"default": Builder(MyRepo)}),
                ]
            ),
            (
                [
                    Dependency(
                        BaseRepo,
                        alias="my-alias",
                        builders={"default": Builder(MyRepo)},
                    ),
                    Dependency(
                        BaseRepo,
                        alias="my-alias",
                        builders={"default": Builder(MyRepo)},
                    ),
                ]
            ),
            (
                [
                    Dependency(alias="my-alias", builders={"default": Builder(MyRepo)}),
                    Dependency(alias="my-alias", builders={"default": Builder(MyRepo)}),
                ]
            ),
        ],
    )
    def should_raise_exception_if_there_is_duplicated_dependencies_when_overwrite_false(
        self, dependencies
    ):
        with pytest.raises(IndexError):
            Container.set_dependencies(dependencies, overwrite=False)

        Container.clear()

    def should_raise_exception_if_repeat_alias_when_overwrite_false(self):
        dependencies = [
            Dependency(
                BaseRepo, alias="my-alias", builders={"default": Builder(MyRepo)}
            ),
            Dependency(
                BaseRepo, alias="my-alias", builders={"default": Builder(MyRepo)}
            ),
        ]

        with pytest.raises(IndexError):
            Container.set_dependencies(dependencies, overwrite=False)

        Container.clear()

    @pytest.mark.parametrize(
        "dependencies,expected_available_dependencies",
        [
            ([], []),
            (
                [Dependency(BaseRepo, builders={"default": Builder(MyRepo)})],
                ["BaseRepo"],
            ),
            (
                [
                    Dependency(BaseRepo, builders={"default": Builder(MyRepo)}),
                    Dependency(
                        alias="inmemory_repo", default_builder=Builder(InMemoryRepo)
                    ),
                ],
                ["BaseRepo", "inmemory_repo"],
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
                    alias="repo-with-dependency",
                    default_builder=Builder(
                        MyRepoWithBuilderAndDependency, is_builder=True
                    ),
                ),
                Dependency(alias="repo", builders={"default": Builder(MyRepo)}),
            ],
            [
                Dependency(alias="repo", builders={"default": Builder(MyRepo)}),
                Dependency(
                    alias="repo-with-dependency",
                    default_builder=Builder(
                        MyRepoWithBuilderAndDependency, is_builder=True
                    ),
                ),
            ],
            [
                Dependency(alias="repo", builders={"default": Builder(MyRepo)}),
                Dependency(alias="other-repo", builders={"default": Builder(MyRepo)}),
                Dependency(
                    alias="repo-with-dependency",
                    default_builder=Builder(
                        MyRepoWithBuilderAndDependency, is_builder=True
                    ),
                ),
                Dependency(
                    alias="repo-with-3-dependencies",
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
        expected_dependencies_names = [dependency.alias for dependency in dependencies]

        Container.set_dependencies(dependencies)

        assert (
            Container.get_available_dependencies().sort()
            == expected_dependencies_names.sort()
        )

        for name in expected_dependencies_names:
            assert isinstance(Container.get(name), BaseRepo)

        Container.clear()
