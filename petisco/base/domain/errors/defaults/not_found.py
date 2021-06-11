from petisco.base.domain.errors.domain_error import DomainError


class NotFound(DomainError):
    def detail(self) -> str:
        return f"Not Found{self.get_message()}"


class ClientNotFound(DomainError):
    def detail(self) -> str:
        return f"Client Not Found{self.get_message()}"


class UserNotFound(DomainError):
    def detail(self) -> str:
        return f"User Not Found{self.get_message()}"
