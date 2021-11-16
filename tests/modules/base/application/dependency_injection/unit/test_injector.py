import pytest

from petisco import Builder, Dependency, Injector
from tests.modules.base.application.dependency_injection.unit.dummy_repositories import (
    InMemoryRepo,
    MyRepo,
    MyRepoWithBuilderAndDependency,
)


@pytest.mark.unit
def test_injector_should_success_when_access_one_dynamic_attr_representing_a_dependency():
    dependencies = [Dependency(name="repo", default_builder=Builder(MyRepo))]

    Injector.set_dependencies(dependencies)

    assert Injector.get_available_dependencies() == ["repo"]

    assert isinstance(Injector().get("repo"), MyRepo)
    assert isinstance(Injector().repo, MyRepo)

    Injector.clear()


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
def test_injector_should_return_several_available_dependencies(
    dependencies, expected_available_dependencies
):

    Injector.set_dependencies(dependencies)

    assert Injector.get_available_dependencies() == expected_available_dependencies

    injector = Injector()
    for available_dependency in expected_available_dependencies:
        assert getattr(injector, available_dependency)

    Injector.clear()


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
    ],
)
def test_injector_should_success_when_add_dependecies_which_depends_from_another_dependency(
    dependencies,
):
    Injector.set_dependencies(dependencies)

    assert Injector.get_available_dependencies() == ["repo", "repo-with-dependency"]

    assert isinstance(Injector().get("repo"), MyRepo)
    assert isinstance(Injector().repo, MyRepo)

    Injector.clear()
