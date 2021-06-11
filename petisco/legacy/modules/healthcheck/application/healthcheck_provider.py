from typing import Dict

from meiga import Result, Error, Failure, Success

from petisco.legacy.application.petisco import Petisco
from petisco.legacy.persistence.persistence import Persistence
from petisco.legacy.use_case.use_case import UseCase
from petisco.legacy.modules.healthcheck.domain.persistence_error import PersistenceError


class HealthcheckProvider(UseCase):
    def execute(self, petisco: Petisco) -> Result[Dict, Error]:

        healthcheck = {
            "app_name": petisco._app_name,
            "app_version": petisco._app_version,
            "persistence_available": Persistence.is_available(),
        }

        if Persistence.exist() and not Persistence.is_available():
            return Failure(PersistenceError("Persistence is not available"))

        return Success(healthcheck)
