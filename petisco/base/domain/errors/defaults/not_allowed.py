from petisco.base.domain.errors.domain_error import DomainError


class NotAllowed(DomainError):
    @classmethod
    def get_specify_detail(cls) -> str:
        return "Not Allowed"
