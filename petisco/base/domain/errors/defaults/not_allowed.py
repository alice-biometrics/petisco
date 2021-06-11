from petisco.base.domain.errors.domain_error import DomainError


class NotAllowed(DomainError):
    def get_specify_detail(self) -> str:
        return "Not Allowed"
