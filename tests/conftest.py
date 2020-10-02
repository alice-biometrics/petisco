from petisco.frameworks.flask.flask_extension_is_installed import (
    flask_extension_is_installed,
)
from petisco.fixtures import *
from .fixtures import *
from tests.modules.event.fixtures import *
from tests.modules.unit.controller.fixtures import *

if "PETISCO_END2END_TESTS" in os.environ:
    from tests.end2end.fixtures import *


if flask_extension_is_installed():
    pass
