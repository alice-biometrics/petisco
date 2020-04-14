from typing import Dict

from meiga import Result, Error, Failure, Success

from petisco.application.petisco import Petisco
from petisco.use_case.use_case import UseCase
from petisco.modules.healthcheck.domain.persistence_error import PersistenceError


class HealthcheckProvider(UseCase):
    def execute(self, petisco: Petisco) -> Result[Dict, Error]:

        healthcheck = {"app_name": petisco.app_name, "app_version": petisco.app_version}

        if petisco.persistence_configured:
            from petisco.persistence.sqlalchemy.sqlalchemy_session_scope import (
                session_scope,
            )

            with session_scope() as session:
                try:
                    session.execute("SELECT 1")
                except Exception as e:
                    return Failure(PersistenceError(str(e)))
            healthcheck["persistence_available"] = True

        return Success(healthcheck)
