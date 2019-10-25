from functools import wraps

from petisco.controller.errors.invalid_token_http_error import InvalidTokenHttpError
from petisco.controller.jwt.jwt_config import JwtConfig


class JwtDecorator(object):
    def __init__(self, jwt_config: JwtConfig = None):
        self.jwt_config = jwt_config

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if not self.jwt_config:
                return func(*args, **kwargs)

            token_info = kwargs.get("token_info")

            if not token_info:
                return InvalidTokenHttpError(
                    suffix="This entry point expects a valid {} Token ".format(
                        self.jwt_config.token_type
                    )
                ).handle()

            client_id = token_info.get("client_id")
            token_type = token_info.get("token_type")
            user_id = token_info.get("user_id")

            if not user_id or user_id == "null":
                user_id = None

            if (
                token_type != self.jwt_config.token_type
                or (self.jwt_config.require_user and not user_id)
                or (not self.jwt_config.require_user and user_id)
            ):
                return InvalidTokenHttpError(
                    suffix="This entry point expects a valid {} Token ".format(
                        self.jwt_config.token_type
                    )
                ).handle()

            del kwargs["token_info"]
            del kwargs["user"]
            if self.jwt_config.require_user:
                return func(client_id, user_id, *args, **kwargs)
            else:
                return func(client_id, *args, **kwargs)

        return wrapper


jwt = JwtDecorator
