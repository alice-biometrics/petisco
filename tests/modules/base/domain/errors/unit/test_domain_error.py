import pytest

from petisco import DomainError


@pytest.mark.unit
class TestDomainError:
    def should_success_constructor(self):
        domain_error = DomainError()

        assert domain_error.detail() == "DomainError"

    def should_success_constructor_with_uuid_value(self):
        domain_error = DomainError(uuid_value="27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4")

        assert (
            domain_error.detail()
            == "DomainError (27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4)"
        )

    def should_success_constructor_with_additional_info(self):
        domain_error = DomainError(additional_info={"additional": "info"})

        assert domain_error.detail() == "DomainError [{'additional': 'info'}]"

    def should_success_constructor_with_uuid_value_and_additional_info(self):
        domain_error = DomainError(
            uuid_value="27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4",
            additional_info={"additional": "info"},
        )

        assert (
            domain_error.detail()
            == "DomainError (27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4) [{'additional': 'info'}]"
        )

    def should_success_constructor_inherit_object(self):
        class MyDomainError(DomainError):
            pass

        domain_error = MyDomainError()

        assert domain_error.detail() == "MyDomainError"

    def should_success_constructor_inherit_object_with_specific_detail(self):
        class MyDomainError(DomainError):
            def detail(self):
                return "my-detail"

        domain_error = MyDomainError()

        assert domain_error.detail() == "my-detail"

    def should_success_constructor_inherit_object_with_deprecated_specify_detail_with_uuid_value(
        self,
    ):
        class MyDomainError(DomainError):
            def get_specific_detail(self):
                return "my-detail"

        domain_error = MyDomainError(uuid_value="27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4")

        assert (
            domain_error.detail() == "my-detail (27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4)"
        )

    def should_success_constructor_inherit_object_with_specific_detail_with_uuid_value(
        self,
    ):
        class MyDomainError(DomainError):
            def get_specific_detail(self):
                return "my-detail"

        domain_error = MyDomainError(uuid_value="27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4")

        assert (
            domain_error.detail() == "my-detail (27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4)"
        )

    def success_defining_auto_specific_detail(self):
        class MyDomainError(DomainError):
            ...

        domain_error = MyDomainError()

        assert domain_error.detail() == "MyDomainError"
