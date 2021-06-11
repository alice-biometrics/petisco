from petisco.base.domain.errors.domain_error import DomainError


class AlreadyExists(DomainError):
    def get_specify_detail(self) -> str:
        return "Already Exists"


class ClientAlreadyExists(DomainError):
    def get_specify_detail(self) -> str:
        return "Client Already Exists"


class UserAlreadyExists(DomainError):
    def get_specify_detail(self) -> str:
        return "User Already Exists"
