import base64
import json


def api_key_info_func(api_key, required_scopes):
    """
    Check and retrieve authentication information from api_key.
    Returned value will be passed in 'token_info' parameter of your operation function, if there is one.
    'sub' or 'uid' will be set in 'user' parameter of your operation function, if there is one.

    :param api_key API key provided by Authorization header
    :type api_key: str
    :param required_scopes Always None. Used for other authentication method
    :type required_scopes: None
    :return: Information attached to provided api_key or None if api_key is invalid or does not allow access to called API
    :rtype: dict | None
    """
    return {"uid": api_key}


def not_implemented_bearer_info_func(token):
    return {}


def bearer_info_func(token):
    """
    Check and retrieve authentication information from custom bearer token.
    Returned value will be passed in 'token_info' parameter of your operation function, if there is one.
    'sub' or 'uid' will be set in 'user' parameter of your operation function, if there is one.

    :param token Token provided by Authorization header
    :type token: str
    :return: Decoded token information or None if token is invalid
    :rtype: dict | None
    """
    token_payload = decode_token_payload(token)
    if not token_payload:
        raise PermissionError("Required token cannot be decoded")

    token_info = {
        "user_id": token_payload.get("sub"),
        "client_id": token_payload.get("cli"),
        "token_type": token_payload.get("typ"),
    }
    return token_info


def decode_token_payload(token):
    try:
        token_payload = token.split(".")[1]
    except IndexError:
        return None
    token_payload += "=" * ((4 - len(token_payload) % 4) % 4)
    return json.loads(base64.b64decode(token_payload).decode("utf-8"))
