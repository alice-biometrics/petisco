from petisco.frameworks.flask.flask_extension_is_installed import (
    flask_extension_is_installed,
)
from .fixtures import *

from petisco.fixtures import *

if flask_extension_is_installed():
    from .integration.flask_app.fixtures import (
        client,
        database,
        given_any_apikey,
        given_auth_token_headers_creator,
        given_code_injection_name,
    )
