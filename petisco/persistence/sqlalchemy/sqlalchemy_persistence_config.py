from typing import Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class SqlAlchemyPersistenceConfig:
    server: str
    database: str
    driver: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[str] = None
