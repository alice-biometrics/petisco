from typing import Callable, List

from sqlalchemy import text


class SqlExecutor:
    def __init__(self, session_scope: Callable):
        self.session_scope = session_scope

    def _get_command(self, statement: str):
        command = text(statement.rstrip("\n"))
        return command

    def execute_from_filename(self, filename: str):
        with open(filename) as file:
            statements = file.read().split(";")
            self.execute_statements(statements)

    def execute_statement(self, statement: str):
        with self.session_scope() as session:
            command = self._get_command(statement)
            session.execute(command)

    def execute_statements(self, statements: List[str]):
        with self.session_scope() as session:
            for statement in statements:
                command = self._get_command(statement)
                session.execute(command)
