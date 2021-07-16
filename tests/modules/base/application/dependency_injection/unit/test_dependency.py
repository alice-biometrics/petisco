import pytest

from petisco import Dependency
from tests.modules.base.application.dependency_injection.unit.dummy_repositories import (
    InMemoryRepo,
    InMemoryRepoBuilder,
    MyRepo,
    MyRepoBuilder,
)


@pytest.mark.unit
def test_dependency_should_return_default_instance():

    dependency = Dependency(
        name="repo",
        default_builder=MyRepoBuilder(),
        envar_modifier="REPOSITORY",
        builders={"inmemory": InMemoryRepoBuilder()},
    )

    assert isinstance(dependency.get_instance(), MyRepo)


@pytest.mark.unit
def test_dependency_should_return_one_instance_from_valid_envar_modifier_value(
    monkeypatch,
):

    monkeypatch.setenv("REPOSITORY", "inmemory")
    dependency = Dependency(
        name="repo",
        default_builder=MyRepoBuilder(),
        envar_modifier="REPOSITORY",
        builders={"inmemory": InMemoryRepoBuilder()},
    )

    assert isinstance(dependency.get_instance(), InMemoryRepo)

    monkeypatch.undo()


@pytest.mark.unit
def test_dependency_should_return_default_if_selected_instanced_by_envar_modifier_value_is_not_available(
    monkeypatch,
):

    monkeypatch.setenv("REPOSITORY", "other")
    dependency = Dependency(
        name="repo",
        default_builder=MyRepoBuilder(),
        envar_modifier="REPOSITORY",
        builders={"inmemory": InMemoryRepoBuilder()},
    )

    assert isinstance(dependency.get_instance(), MyRepo)

    monkeypatch.undo()


@pytest.mark.unit
def test_dependency_should_return_default_when_optional_parameters_are_not_used(
    monkeypatch,
):

    dependency = Dependency(name="repo", default_builder=MyRepoBuilder())

    assert isinstance(dependency.get_instance(), MyRepo)
