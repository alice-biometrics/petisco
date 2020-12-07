import os


class MySqlConnection:
    def __init__(
        self,
        server_name: str,
        driver: str,
        user: str,
        password: str,
        host: str,
        port: str,
        database_name: str,
        url: str,
    ):
        self.server_name = server_name
        self.driver = driver
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name
        self.url = url

    @staticmethod
    def create(
        server_name: str = "mysql",
        driver: str = "pymysql",
        user: str = "root",
        password: str = "root",
        host: str = "mysql",
        port: str = "3306",
        database_name: str = "petisco-default-db",
    ):
        url = (
            f"{server_name}+{driver}://{user}:{password}@{host}:{port}/{database_name}"
        )
        return MySqlConnection(
            server_name, driver, user, password, host, port, database_name, url
        )

    @staticmethod
    def create_local():
        return MySqlConnection.create(host="localhost", port="3307")

    @staticmethod
    def from_environ():
        return MySqlConnection.create(
            "mysql",
            "pymysql",
            os.getenv("MYSQL_USER", "root"),
            os.getenv("MYSQL_PASSWORD", "root"),
            os.getenv("MYSQL_HOST", "mysql"),
            os.getenv("MYSQL_PORT", "3306"),
            os.getenv("MYSQL_DATABASE", "petisco-default-db"),
        )
