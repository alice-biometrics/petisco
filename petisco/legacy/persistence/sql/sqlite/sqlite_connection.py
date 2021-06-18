class SqliteConnection:
    def __init__(self, server_name: str, database_name: str, url: str):
        self.server_name = server_name
        self.database_name = database_name
        self.url = url

    @staticmethod
    def create(server_name: str, database_name: str):
        url = f"{server_name}:///{database_name}"
        return SqliteConnection(server_name, database_name, url)
