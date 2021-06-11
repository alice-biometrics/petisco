from petisco.base.domain.errors.domain_error import DomainError


class AlreadyExists(DomainError):
    def detail(self) -> str:
        return f"Already Exists{self.get_message()}"


class ClientAlreadyExists(DomainError):
    def detail(self) -> str:
        return f"Client Already Exists{self.get_message()}"


class UserAlreadyExists(DomainError):
    def detail(self) -> str:
        return f"User Already Exists{self.get_message()}"
