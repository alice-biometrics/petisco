from typing import Dict

from meiga import Result, Error, Failure, Success

from petisco.application.petisco import Petisco
from petisco.use_case.use_case import UseCase
from petisco.modules.healthcheck.domain.persistence_error import PersistenceError


class HealthcheckProvider(UseCase):
    def execute(self, petisco: Petisco) -> Result[Dict, Error]:

        healthcheck = {
            "app_name": petisco._app_name,
            "app_version": petisco._app_version,
        }

        if petisco.persistence_sources:
            from petisco.persistence.sqlalchemy.sqlalchemy_session_scope import (
                session_scope,
            )

            for (
                persistence_source_name,
                persistence_source,
            ) in petisco.persistence_sources.items():
                if persistence_source["type"] == "sql":
                    with session_scope(persistence_source_name) as session:
                        try:
                            session.execute("SELECT 1")
                        except Exception as e:
                            return Failure(PersistenceError(str(e)))
            healthcheck["persistence_available"] = True

        return Success(healthcheck)
