from typing import Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class PyMongoPersistenceConfig:
    user: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    database: Optional[str] = None
    port: Optional[int] = 27017
