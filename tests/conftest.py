from petisco.frameworks.flask.flask_extension_is_installed import (
    flask_extension_is_installed,
)
from petisco.fixtures import *
from .fixtures import *
from tests.modules.event.fixtures import *
from tests.modules.unit.controller.fixtures import *
from tests.end2end.fixtures import *


if flask_extension_is_installed():
    pass
