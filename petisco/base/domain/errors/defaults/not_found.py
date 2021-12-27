from petisco.base.domain.errors.domain_error import DomainError
from petisco.base.domain.model.uuid import Uuid


class NotFound(DomainError):
    def get_specify_detail(self) -> str:
        return "Not Found"


class ClientNotFound(DomainError):
    def get_specify_detail(self) -> str:
        return "Client Not Found"


class UserNotFound(DomainError):
    def get_specify_detail(self) -> str:
        return "User Not Found"


class AggregateNotFoundError(DomainError):
    def __init__(self, repository_name: str = None, entity_id: Uuid = None):
        entity_id_str = f" ({entity_id.value})" if entity_id else ""
        repository_str = f" (repository: {repository_name})" if repository_name else ""
        message = f"Entity{entity_id_str} not found{repository_str}"

        super().__init__(
            uuid_value=entity_id.value, additional_info={"message": message}
        )

    def get_specify_detail(self) -> str:
        return "Aggregate not found error"


class AggregatesNotFoundError(DomainError):
    def __init__(self, repository_name: str = None):
        repository_str = f" (repository: {repository_name})" if repository_name else ""
        message = f"Entities not found{repository_str}]"
        super().__init__(additional_info={"message": message})

    def get_specify_detail(self) -> str:
        return "Aggregates not found error"
