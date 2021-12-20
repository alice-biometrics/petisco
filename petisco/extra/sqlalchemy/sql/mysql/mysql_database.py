from typing import Callable, List

from sqlalchemy.orm import scoped_session

from petisco.base.domain.persistence.interface_database import Database
from petisco.base.domain.persistence.persistence_models import PersistenceModels
from petisco.extra.sqlalchemy.sql.mysql.mysql_connection import MySqlConnection
from petisco.extra.sqlalchemy.sql.sql_session_scope_provider import (
    sql_session_scope_provider,
)


class MySqlDatabase(Database):
    @staticmethod
    def local_connection_checker():
        return MySqlDatabase(
            name="test", connection=MySqlConnection.create_local("test")
        )

    def __init__(
        self,
        name: str,
        connection: MySqlConnection,
        model_filename: str = None,
        print_sql_statements: bool = False,
        use_scoped_session: bool = True,
        use_future: bool = True,
    ):
        if not connection or not isinstance(connection, MySqlConnection):
            raise ConnectionError(
                "MySqlDatabase needs a valid MySqlConnection connection"
            )
        if model_filename:
            self.persistence_models = PersistenceModels.from_filename(model_filename)
        else:
            self.persistence_models = PersistenceModels(models={})
        self.connection = connection
        self.print_sql_statements = print_sql_statements
        self.use_scoped_session = use_scoped_session
        self.use_future = use_future

        super().__init__(name, self.persistence_models.models)
        self._init()

    def _init(self):
        from sqlalchemy.ext.declarative import declarative_base

        self.base = declarative_base()

    def create(self):
        self.persistence_models.import_models()
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy_utils import create_database, database_exists

        engine = create_engine(
            self.connection.url,
            pool_pre_ping=True,
            json_serializer=lambda obj: obj,
            json_deserializer=lambda obj: obj,
            echo=self.print_sql_statements,
            future=self.use_future,
        )

        if not database_exists(engine.url):
            create_database(engine.url)
            self.base.metadata.create_all(engine)

        self.session_maker = sessionmaker(bind=engine, future=self.use_future)

    def delete(self):
        pass
        # os.remove(self.connection.database_name)

    def clear_data(self):
        # Not available yet to avoid production problems.
        # This, needs to be well documented.
        # self.base.metadata.drop_all(self.engine)
        pass

    def is_available(self):
        try:
            session_scope = self.get_session_scope()
            with session_scope() as session:
                session.execute("SELECT 1")
                _is_available = True
        except Exception:  # noqa E722
            _is_available = False
        return _is_available

    def get_base(self):
        return self.base

    def get_model(self, model_name: str):
        model = self.persistence_models.get_imported_models().get(model_name)
        if not model:
            raise IndexError(
                f'Model "{model_name}" is not available for "{self.name}" database'
            )
        return model

    def get_model_names(self) -> List[str]:
        return list(self.persistence_models.get_models_names().keys())

    def get_session(self):
        if self.use_scoped_session:
            Session = scoped_session(self.session_maker)  # noqa
        else:
            Session = self.session_maker
        return Session

    def get_session_scope(self) -> Callable:
        return sql_session_scope_provider(self.get_session())
