from petisco.base.domain.errors.domain_error import DomainError
from petisco.base.domain.model.uuid import Uuid


class AlreadyExists(DomainError):
    def get_specify_detail(self) -> str:
        return "Already Exists"


class ClientAlreadyExists(DomainError):
    def get_specify_detail(self) -> str:
        return "Client Already Exists"


class UserAlreadyExists(DomainError):
    def get_specify_detail(self) -> str:
        return "User Already Exists"


class AggregateAlreadyExistError(DomainError):
    def __init__(
        self,
        repository_name: str = None,
        table_name: str = None,
        aggregate_id: Uuid = None,
    ):
        aggregate_id_str = f" ({aggregate_id.value})" if aggregate_id else ""
        repository_str = f" (repository: {repository_name})" if repository_name else ""
        table_str = f" (table: {table_name})" if repository_name else ""
        message = (
            f"Aggregate{aggregate_id_str} already exist{repository_str}{table_str}"
        )
        super().__init__(
            uuid_value=aggregate_id.value, additional_info={"message": message}
        )

    def get_specify_detail(self) -> str:
        return "Aggregate already exist error"
