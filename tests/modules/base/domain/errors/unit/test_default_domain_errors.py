from typing import Type

import pytest

from petisco import (
    AggregateAlreadyExistError,
    AggregateNotFoundError,
    AggregatesNotFoundError,
    AlreadyExists,
    ClientAlreadyExists,
    ClientNotFound,
    InvalidUuid,
    InvalidValueObject,
    NotFound,
    Uuid,
)


@pytest.mark.unit
class TestDefaultDomainErrors:
    @pytest.mark.parametrize(
        "type_domain_error",
        [
            NotFound,
            AlreadyExists,
            ClientNotFound,
            ClientAlreadyExists,
            InvalidUuid,
            InvalidValueObject,
        ],
    )
    def should_success_aliase_domain_error_constructor(self, type_domain_error: Type):
        domain_error = type_domain_error()
        assert domain_error.detail() == domain_error.__class__.__name__

    @pytest.mark.parametrize(
        "repository_name,aggregate_id",
        [
            (None, None),
            ("my-repository", None),
            (None, Uuid.v4()),
            ("my-repository", Uuid.v4()),
        ],
    )
    def should_success_aggregate_not_found_error_constructor(
        self, repository_name, aggregate_id
    ):
        domain_error = AggregateNotFoundError(repository_name, aggregate_id)
        assert "AggregateNotFoundError" in domain_error.detail()

    @pytest.mark.parametrize("repository_name", [None, "my-repository"])
    def should_success_aggregates_not_found_error_constructor(self, repository_name):
        domain_error = AggregatesNotFoundError(repository_name)
        assert "AggregatesNotFoundError" in domain_error.detail()

    @pytest.mark.parametrize("repository_name", [None, "my-repository"])
    def should_success_aggregate_already_exist_error_constructor(self, repository_name):
        domain_error = AggregateAlreadyExistError(repository_name)
        assert "AggregateAlreadyExistError" in domain_error.detail()
