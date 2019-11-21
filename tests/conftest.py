from petisco.frameworks.flask.flask_extension_is_installed import (
    flask_extension_is_installed,
)

if flask_extension_is_installed():
    from .integration.controller.fixtures import (
        client,
        database,
        given_any_apikey,
        given_auth_token_headers_creator,
        given_any_name,
        given_code_injection_name,
        given_any_user_id,
    )
