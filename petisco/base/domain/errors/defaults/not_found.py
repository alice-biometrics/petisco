from typing import Optional

from petisco.base.domain.errors.domain_error import DomainError
from petisco.base.domain.model.uuid import Uuid


class NotFound(DomainError):
    ...


class ClientNotFound(DomainError):
    ...


class UserNotFound(DomainError):
    ...


class AggregateNotFoundError(DomainError):
    def __init__(self, aggregate_id: Uuid, repository_name: Optional[str] = None):
        aggregate_id_str = f" ({aggregate_id.value})" if aggregate_id else ""
        repository_str = f" (repository: {repository_name})" if repository_name else ""
        message = f"Aggregate{aggregate_id_str} not found{repository_str}"
        uuid_value = aggregate_id.value if aggregate_id else None
        super().__init__(uuid_value=uuid_value, additional_info={"message": message})


class AggregatesNotFoundError(DomainError):
    def __init__(self, repository_name: str = None):
        repository_str = f" (repository: {repository_name})" if repository_name else ""
        message = f"Aggregates not found{repository_str}]"
        super().__init__(additional_info={"message": message})
