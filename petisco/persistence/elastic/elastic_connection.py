import os


class ElasticConnection:
    def __init__(
        self,
        username: str = None,
        password: str = None,
        host: str = "http://localhost",
        port: str = "9200",
    ):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    @property
    def http_auth(self):
        http_auth = None
        if self.username and self.password:
            http_auth = (self.username, self.password)
        return http_auth

    @staticmethod
    def create(username: str, password: str, host: str, port: str):
        return ElasticConnection(username, password, host, port)

    @staticmethod
    def create_local():
        return ElasticConnection(host="http://localhost")

    @staticmethod
    def from_environ():
        return ElasticConnection.create(
            os.getenv("ELASTIC_USERNAME", ""),
            os.getenv("ELASTIC_PASSWORD", ""),
            os.getenv("ELASTIC_HOST", "http://localhost"),
            os.getenv("ELASTIC_PORT", "9200"),
        )

    def to_elastic_format(self):
        if self.host.startswith("http"):
            return [f"{self.host}:{self.port}"]
        else:
            return [{"host": self.host, "port": self.port}]
