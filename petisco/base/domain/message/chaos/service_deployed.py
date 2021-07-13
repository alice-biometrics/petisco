from petisco.base.domain.message.domain_event import DomainEvent


class ServiceDeployed(DomainEvent):
    app_name: str
    app_version: str
