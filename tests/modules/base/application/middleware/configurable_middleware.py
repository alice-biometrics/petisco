from meiga import AnyResult

from petisco import Middleware


class ConfigurableMiddleware(Middleware):
    def __init__(self, configurable_message_before: str, configurable_message_after: str):
        self.configurable_message_before = configurable_message_before
        self.configurable_message_after = configurable_message_after

    def before(self) -> None:
        print(f"configurable_message_before={self.configurable_message_before}")

    def after(self, result: AnyResult) -> None:
        print(f"configurable_message_after={self.configurable_message_after}")
