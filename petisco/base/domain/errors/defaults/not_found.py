from petisco.base.domain.errors.domain_error import DomainError


class NotFound(DomainError):
    def get_specify_detail(self) -> str:
        return "Not Found"


class ClientNotFound(DomainError):
    def get_specify_detail(self) -> str:
        return "Client Not Found"


class UserNotFound(DomainError):
    def get_specify_detail(self) -> str:
        return "User Not Found"
