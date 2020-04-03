from typing import Dict

from meiga import Result, Error, Failure, Success

from petisco.use_case.use_case import UseCase
from petisco.application.application_config import ApplicationConfig
from petisco.modules.healthcheck.domain.persistence_error import PersistenceError
from petisco.persistence.sqlalchemy.sqlalchemy_session_scope import session_scope


class HealthcheckProvider(UseCase):
    def execute(self, application_config: ApplicationConfig) -> Result[Dict, Error]:

        healthcheck = {
            "app_name": application_config.app_name,
            "app_version": application_config.app_version,
            "mode": application_config.mode,
        }

        if application_config.persistence_configured:
            with session_scope() as session:
                try:
                    session.execute("SELECT 1")
                except Exception as e:
                    return Failure(PersistenceError(str(e)))
            healthcheck["persistence_available"] = True

        return Success(healthcheck)
