from meiga import Result

from petisco.legacy import controller_handler
from tests.end2end.flask_app.users_count.application.users_count_retriever import (
    UsersCountRetriever,
)


def success_handler(result: Result):
    return {"users_count": result.value}, 200


@controller_handler(success_handler=success_handler)
def get_users_count():
    return UsersCountRetriever.build().execute()
