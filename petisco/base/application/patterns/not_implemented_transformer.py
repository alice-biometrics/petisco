from typing import Any

from meiga import Error, Result, Success

from petisco.base.application.patterns.transformer import Transformer


class NotImplementedTransformer(Transformer):
    def get_domain_model(self, infrastructure_model: Any) -> Result[Any, Error]:
        return Success(infrastructure_model)

    def get_infrastructure_model(self, domain_model: Any) -> Result[Any, Error]:
        return Success(domain_model)
