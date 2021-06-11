from petisco.base.domain.errors.domain_error import DomainError


class NotAllowed(DomainError):
    def detail(self) -> str:
        return f"Not Allowed{self.get_message()}"
