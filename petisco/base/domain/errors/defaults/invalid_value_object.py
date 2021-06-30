from petisco.base.domain.errors.domain_error import DomainError


class InvalidValueObject(DomainError):
    def get_specify_detail(self) -> str:
        return "Invalid ValueObject"
