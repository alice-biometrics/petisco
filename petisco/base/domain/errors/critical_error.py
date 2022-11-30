from petisco.base.domain.errors.domain_error import DomainError


class CriticalError(DomainError):
    """
    A base class to define critical errors.

    If you inherit from CriticalError and uses NotifierMiddleware in your operations (Controllers or Subscribers), when
    you UseCase fails with these errors the system will notify the issue.
    """

    ...
