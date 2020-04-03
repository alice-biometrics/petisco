import json
from typing import Dict

from healthcheck import EnvironmentDump
from meiga import Result, Error, Success, Failure

from petisco.modules.environment.domain.environment_provider_error import (
    EnvironmentProviderError,
)
from petisco.use_case.use_case import UseCase
from petisco.application.application_config import ApplicationConfig


class EnvironmentProvider(UseCase):
    def __init__(
        self,
        include_python: bool = True,
        include_os: bool = True,
        include_process: bool = True,
    ):
        self.include_python = include_python
        self.include_os = include_os
        self.include_process = include_process

    def execute(self, application_config: ApplicationConfig) -> Result[Dict, Error]:
        try:
            application_info = {"config": application_config.info}
            envdump = EnvironmentDump(
                include_python=self.include_python,
                include_os=self.include_os,
                include_process=self.include_process,
            )
            envdump.add_section("Environment", application_info)
            envdump_result = envdump.run()
        except Exception as e:
            return Failure(EnvironmentProviderError(str(e)))
        return Success(json.loads(envdump_result[0]))
