from __future__ import annotations

from typing import Callable, ContextManager

from sqlalchemy import text
from sqlalchemy.orm import Session


class SqlExecutor:
    def __init__(self, session_scope: Callable[..., ContextManager[Session]]):
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

    def execute_statements(self, statements: list[str]):
        with self.session_scope() as session:
            for statement in statements:
                command = self._get_command(statement)
                session.execute(command)
