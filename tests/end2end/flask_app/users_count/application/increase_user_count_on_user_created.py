from meiga import Result, Error

from petisco.legacy import Event
from tests.end2end.flask_app.users_count.application.users_count_increaser import (
    UserCountIncreaser,
)


def increase_user_count_on_user_created(event: Event) -> Result[bool, Error]:
    return UserCountIncreaser.build().execute()
