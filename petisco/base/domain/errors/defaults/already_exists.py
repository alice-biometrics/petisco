from typing import Optional

from petisco.base.domain.errors.domain_error import DomainError
from petisco.base.domain.model.uuid import Uuid


class AlreadyExists(DomainError):
    ...


class ClientAlreadyExists(DomainError):
    ...


class UserAlreadyExists(DomainError):
    ...


class AggregateAlreadyExistError(DomainError):
    def __init__(
        self,
        aggregate_id: Uuid,
        repository_name: Optional[str] = None,
        table_name: Optional[str] = None,
    ):
        aggregate_id_str = f" ({aggregate_id.value})" if aggregate_id else ""
        repository_str = f" (repository: {repository_name})" if repository_name else ""
        table_str = f" (table: {table_name})" if repository_name else ""
        message = (
            f"Aggregate{aggregate_id_str} already exist{repository_str}{table_str}"
        )
        uuid_value = aggregate_id.value if aggregate_id else None
        super().__init__(uuid_value=uuid_value, additional_info={"message": message})
