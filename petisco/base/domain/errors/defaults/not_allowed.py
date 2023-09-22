from petisco.base.domain.errors.domain_error import DomainError


class NotAllowed(DomainError):
    def get_specific_detail(cls) -> str:
        return "Not Allowed"
