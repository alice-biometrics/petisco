from petisco.base.domain.errors.domain_error import DomainError


class InvalidUuid(DomainError):
    def detail(self) -> str:
        return f"Invalid Uuid{self.get_message()}"
