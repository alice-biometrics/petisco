import pytest

from petisco import Builder, Dependency
from tests.modules.base.application.dependency_injection.unit.dummy_repositories import (
    BaseRepo,
    InMemoryRepo,
    MyGenericRepo,
    MyRepo,
)


@pytest.mark.unit
class TestDependency:
    def should_return_default_instance(self):

        dependency = Dependency(
            BaseRepo,
            envar_modifier="REPOSITORY",
            builders={"default": Builder(MyRepo), "inmemory": Builder(InMemoryRepo)},
        )
        assert isinstance(dependency.get_instance(), MyRepo)

    def should_return_one_instance_from_valid_envar_modifier_value(
        self,
        monkeypatch,
    ):

        monkeypatch.setenv("REPOSITORY", "inmemory")
        dependency = Dependency(
            BaseRepo,
            envar_modifier="REPOSITORY",
            builders={"default": Builder(MyRepo), "inmemory": Builder(InMemoryRepo)},
        )

        assert isinstance(dependency.get_instance(), InMemoryRepo)

        monkeypatch.undo()

    def should_return_default_if_selected_instanced_by_envar_modifier_value_is_not_available(
        self,
        monkeypatch,
    ):

        monkeypatch.setenv("REPOSITORY", "other")
        dependency = Dependency(
            BaseRepo,
            envar_modifier="REPOSITORY",
            builders={"default": Builder(MyRepo), "inmemory": Builder(InMemoryRepo)},
        )

        assert isinstance(dependency.get_instance(), MyRepo)

        monkeypatch.undo()

    def should_return_default_when_optional_parameters_are_not_used(self):

        dependency = Dependency(BaseRepo, builders={"default": Builder(MyRepo)})

        assert isinstance(dependency.get_instance(), MyRepo)

    def should_return_default_when_optional_parameters_are_used_but_no_backup_builders_are_defined(
        self,
        monkeypatch,
    ):

        monkeypatch.setenv("REPOSITORY", "other")
        dependency = Dependency(
            BaseRepo,
            envar_modifier="REPOSITORY",
            builders={"default": Builder(MyRepo)},
        )

        assert isinstance(dependency.get_instance(), MyRepo)

        monkeypatch.undo()

    def should_return_typed_default_instance(self):

        dependency = Dependency(BaseRepo, builders={"default": Builder(MyRepo)})

        instance = dependency.get_instance()

        assert dependency.type == BaseRepo
        assert isinstance(instance, MyRepo)

    def should_raise_error_when_default_builder_type_is_not_a_subclass_of_generic_type(
        self,
    ):

        dependency = Dependency(BaseRepo, builders={"default": Builder(str)})

        with pytest.raises(TypeError):
            dependency.get_instance()

    def should_raise_error_when_builder_type_is_not_a_subclass_of_generic_type(self):

        dependency = Dependency(
            BaseRepo,
            builders={
                "default": Builder(MyRepo),
                "inmemory": Builder(InMemoryRepo),
                "invalid": Builder(str),
            },
        )

        with pytest.raises(TypeError):
            dependency.get_instance()

    def should_not_raise_error_when_builder_type_is_not_a_subclass_of_generic_type_with_strict_false(
        self,
    ):

        dependency = Dependency(
            BaseRepo,
            builders={
                "default": Builder(MyRepo),
                "inmemory": Builder(InMemoryRepo),
                "invalid": Builder(str),
            },
            strict=False,
        )

        dependency.get_instance()

    def should_check_default_envar_modifier(self):

        dependency = Dependency(BaseRepo, builders={"default": Builder(MyRepo)})

        assert dependency.envar_modifier == "BASE_REPO_TYPE"

    def should_raise_error_when_no_default_builder_is_given(self):
        with pytest.raises(TypeError):
            Dependency(BaseRepo)

    def should_raise_error_when_no_default_builders_is_given(self):
        with pytest.raises(TypeError):
            Dependency(BaseRepo, builders={"inmemory": Builder(InMemoryRepo)})

    def should_return_default_instance_when_use_generic_class(self):
        dependency = Dependency(
            BaseRepo,
            builders={"default": Builder(MyGenericRepo[int])},
        )
        assert isinstance(dependency.get_instance(), MyGenericRepo)
