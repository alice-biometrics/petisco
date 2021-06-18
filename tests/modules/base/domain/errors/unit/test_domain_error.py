import pytest

from petisco import DomainError


@pytest.mark.unit
def test_domain_error_should_success_constructor():
    domain_error = DomainError()

    assert domain_error.detail() == "DomainError"


@pytest.mark.unit
def test_domain_error_should_success_constructor_with_uuid_value():
    domain_error = DomainError(uuid_value="27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4")

    assert domain_error.detail() == "DomainError (27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4)"


@pytest.mark.unit
def test_domain_error_should_success_constructor_with_additional_info():
    domain_error = DomainError(additional_info={"additional": "info"})

    assert domain_error.detail() == "DomainError [{'additional': 'info'}]"


@pytest.mark.unit
def test_domain_error_should_success_constructor_with_uuid_value_and_additional_info():
    domain_error = DomainError(
        uuid_value="27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4",
        additional_info={"additional": "info"},
    )

    assert (
        domain_error.detail()
        == "DomainError (27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4) [{'additional': 'info'}]"
    )


@pytest.mark.unit
def test_domain_error_should_success_constructor_inherit_object():
    class MyDomainError(DomainError):
        pass

    domain_error = MyDomainError()

    assert domain_error.detail() == "DomainError"


@pytest.mark.unit
def test_domain_error_should_success_constructor_inherit_object_with_specific_detail():
    class MyDomainError(DomainError):
        def detail(self):
            return "my-detail"

    domain_error = MyDomainError()

    assert domain_error.detail() == "my-detail"


@pytest.mark.unit
def test_domain_error_should_success_constructor_inherit_object_with_specific_detail_with_uuid_value():
    class MyDomainError(DomainError):
        def get_specify_detail(self):
            return "my-detail"

    domain_error = MyDomainError(uuid_value="27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4")

    assert domain_error.detail() == "my-detail (27Fdce4B-0550-419B-8364-F5C2Ef0Bd0C4)"
