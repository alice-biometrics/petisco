import os

import pytest

from petisco.application.petisco import Petisco


@pytest.fixture
def petisco_sql_database(execution_path="."):

    if Petisco.get_instance().persistence_configured:

        from sqlalchemy import create_engine
        from petisco.persistence.sqlalchemy.sqlalchemy_persistence import (
            SqlAlchemyPersistence,
        )

        sql_database = os.environ.get("SQL_DATABASE")
        if not sql_database:
            raise RuntimeError(
                "Please add required SQL_DATABASE env variable (e.g pytest.ini, pytest.end2end.ini)"
            )

        Base = SqlAlchemyPersistence.get_instance().base
        Session = SqlAlchemyPersistence.get_instance().session
        connection = f"sqlite:///{sql_database}"
        engine = create_engine(connection)
        Base.metadata.create_all(engine)

        yield

        session = Session()
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)
        os.remove(os.path.join(execution_path, sql_database))
