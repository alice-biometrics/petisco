import os

import pytest

from petisco.application.petisco import Petisco


@pytest.fixture
def petisco_sql_database(request):
    persistence_source_marker = request.node.get_closest_marker("persistence_source")
    if persistence_source_marker is None:
        persistence_source_name = "petisco"
    else:
        persistence_source_name = persistence_source_marker.args[0]

    try:
        petisco = Petisco.get_instance()
        persistence_source_config = petisco.persistence_sources[persistence_source_name]
    except ImportError as e:
        raise ImportError(
            f"{e}\n petisco_sql_database needs a preconfigured Petisco to have available Model definitions"
        )
    except KeyError as e:
        raise KeyError(
            f"{e}\n petisco_sql_database needs a preconfigured Petisco with persistence. Required persistence ({persistence_source_name}) is not available"
        )

    if not persistence_source_config or not persistence_source_config["configured"]:
        yield
    else:
        from sqlalchemy import create_engine
        from petisco.persistence.sqlalchemy.sqlalchemy_persistence import (
            SqlAlchemyPersistence,
        )

        sql_database = os.environ.get("SQL_DATABASE")
        if not sql_database:
            raise RuntimeError(
                "Please add required SQL_DATABASE env variable (e.g pytest.ini, pytest.end2end.ini)"
            )

        Base = SqlAlchemyPersistence.get_instance().sources[persistence_source_name][
            "base"
        ]
        Session = SqlAlchemyPersistence.get_instance().sources[persistence_source_name][
            "session"
        ]
        connection = f"sqlite:///{sql_database}"
        engine = create_engine(connection)
        Base.metadata.create_all(engine)

        yield

        session = Session()
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)
        os.remove(sql_database)
