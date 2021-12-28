import pytest

from petisco import Builder, Container, Dependency
from tests.modules.base.application.dependency_injection.unit.dummy_repositories import (
    InMemoryRepo,
    MyRepo,
    MyRepoWithBuilderAndDependency,
    MyRepoWithBuilderAndSeveralDependency,
    Repo,
)


@pytest.mark.unit
def test_container_should_success_when_access_one_dynamic_attr_representing_a_dependency():
    dependencies = [Dependency(name="repo", default_builder=Builder(MyRepo))]

    Container.set_dependencies(dependencies)

    assert Container.get_available_dependencies() == ["repo"]

    assert isinstance(Container().get("repo"), MyRepo)

    Container.clear()


@pytest.mark.unit
@pytest.mark.parametrize(
    "dependencies,expected_available_dependencies",
    [
        ([], []),
        ([Dependency(name="repo", default_builder=Builder(MyRepo))], ["repo"]),
        (
            [
                Dependency(name="repo", default_builder=Builder(MyRepo)),
                Dependency(name="inmemory_repo", default_builder=Builder(InMemoryRepo)),
            ],
            ["repo", "inmemory_repo"],
        ),
    ],
)
def test_container_should_return_several_available_dependencies(
    dependencies, expected_available_dependencies
):

    Container.set_dependencies(dependencies)

    assert Container.get_available_dependencies() == expected_available_dependencies

    Container.clear()


@pytest.mark.unit
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
def test_container_should_success_when_add_dependecies_which_depends_from_another_dependency(
    dependencies,
):
    expected_dependencies_names = [dependency.name for dependency in dependencies]

    Container.set_dependencies(dependencies)

    assert (
        Container.get_available_dependencies().sort()
        == expected_dependencies_names.sort()
    )

    for name in expected_dependencies_names:
        assert isinstance(Container().get(name), Repo)

    Container.clear()
