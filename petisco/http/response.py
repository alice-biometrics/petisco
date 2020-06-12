from typing import Any

from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Response(object):
    status_code: int
    content: None = field(default=None)
    headers: Any = None
