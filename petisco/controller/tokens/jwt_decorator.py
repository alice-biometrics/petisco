from functools import wraps

from meiga import Failure

from petisco.controller.tokens.token_manager import TokenManager
from petisco.controller.tokens.jwt_errors import InvalidTokenError


class JwtDecorator(object):
    def __init__(self, token_manager: TokenManager = None):
        self.jwt_config = token_manager

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if not self.jwt_config:
                return func(*args, **kwargs)

            auth_token = kwargs.get("headers", {}).get("Authorization")

            token = self.jwt_config.token_decoder.execute(auth_token)

            if token.is_failure:
                # token_info = kwargs.get("token_info")
                # if not token_info:
                return Failure(
                    InvalidTokenError(
                        message=f"This entry point expects a valid {self.jwt_config.token_type} Token"
                    )
                )
            token = token.value

            # client_id = token_info.get("client_id")
            # token_type = token_info.get("token_type")
            # user_id = token_info.get("user_id")

            if (
                token.token_type != self.jwt_config.token_type
                or (self.jwt_config.require_user and not token.user_id)
                or (not self.jwt_config.require_user and token.user_id)
            ):
                return Failure(
                    InvalidTokenError(
                        message=f"This entry point expects a valid {self.jwt_config.token_type} Token"
                    )
                )

            # del kwargs["token_info"]
            #
            # info_id = InfoId.from_strings(
            #     client_id, user_id if self.jwt_config.require_user else None
            # )
            # import pdb; pdb.set_trace()
            # info_id = InfoId.from_token(token)
            # kwargs = dict(kwargs, info_id=info_id)
            return func(*args, **kwargs)

        return wrapper


jwt = JwtDecorator
