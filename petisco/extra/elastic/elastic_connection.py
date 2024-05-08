import os
from typing import Dict, List, Optional, Tuple, Union


class ElasticConnection:
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: str = "http://localhost",
        port: str = "9200",
    ):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    @property
    def http_auth(self) -> Union[Tuple[str, str], None]:
        http_auth = None
        if self.username and self.password:
            http_auth = (self.username, self.password)
        return http_auth

    @staticmethod
    def create(username: str, password: str, host: str, port: str) -> "ElasticConnection":
        return ElasticConnection(username, password, host, port)

    @staticmethod
    def create_local() -> "ElasticConnection":
        return ElasticConnection(host="http://localhost")

    @staticmethod
    def from_environ() -> "ElasticConnection":
        return ElasticConnection.create(
            os.getenv("ELASTIC_USERNAME", ""),
            os.getenv("ELASTIC_PASSWORD", ""),
            os.getenv("ELASTIC_HOST", "http://localhost"),
            os.getenv("ELASTIC_PORT", "9200"),
        )

    def to_elastic_format(self) -> Union[List[str], List[Dict[str, str]]]:
        if self.host.startswith("http"):
            return [f"{self.host}:{self.port}"]
        else:
            return [{"host": self.host, "port": self.port}]
