from typing import Dict, Type

from petisco.base.application.controller.http_error import HttpError
from petisco.base.domain.errors.domain_error import DomainError

ErrorMap = Dict[Type[DomainError], HttpError]
