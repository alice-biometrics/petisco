from petisco.frameworks.flask.flask_extension_is_installed import (
    flask_extension_is_installed,
)

if flask_extension_is_installed():
    from .integration.controller.fixtures import client, given_any_apikey
