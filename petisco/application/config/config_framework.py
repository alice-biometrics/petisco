from typing import Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ConfigFramework:
    selected_framework: str
    config_file: str
    port: Optional[str]
    port_env: Optional[str]
