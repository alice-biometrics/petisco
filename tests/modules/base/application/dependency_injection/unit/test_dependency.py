from abc import ABC, abstractmethod

import pytest

from petisco import Dependency


class Repo(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError


class MyRepo(Repo):
    def execute(self):
        print("MyRepo")


class InMemoryRepo(Repo):
    def execute(self):
        print("InMemoryRepo")


@pytest.mark.unit
def test_dependency_should_return_default_instance():

    dependency = Dependency(
        name="repo",
        default_instance=MyRepo(),
        envar_modifier="REPOSITORY",
        instances={"inmemory": InMemoryRepo()},
    )

    assert isinstance(dependency.get_instance(), MyRepo)


@pytest.mark.unit
def test_dependency_should_return_one_instance_from_valid_envar_modifier_value(
    monkeypatch
):

    monkeypatch.setenv("REPOSITORY", "inmemory")
    dependency = Dependency(
        name="repo",
        default_instance=MyRepo(),
        envar_modifier="REPOSITORY",
        instances={"inmemory": InMemoryRepo()},
    )

    assert isinstance(dependency.get_instance(), InMemoryRepo)

    monkeypatch.undo()


@pytest.mark.unit
def test_dependency_should_return_default_if_selected_instanced_by_envar_modifier_value_is_not_available(
    monkeypatch
):

    monkeypatch.setenv("REPOSITORY", "other")
    dependency = Dependency(
        name="repo",
        default_instance=MyRepo(),
        envar_modifier="REPOSITORY",
        instances={"inmemory": InMemoryRepo()},
    )

    assert isinstance(dependency.get_instance(), MyRepo)

    monkeypatch.undo()


@pytest.mark.unit
def test_dependency_should_return_default_when_optional_parameters_are_not_used(
    monkeypatch
):

    dependency = Dependency(name="repo", default_instance=MyRepo())

    assert isinstance(dependency.get_instance(), MyRepo)
