from fnmatch import fnmatch


class SpecificQueueConfig:
    @staticmethod
    def from_dict(kdict: dict, default_retry_ttl: int, default_main_ttl: int):
        return SpecificQueueConfig(
            wildcard=kdict.get("when_queue_contains", None),
            specific_retry_ttl=kdict.get("use", {}).get("retry_ttl", default_retry_ttl),
            specific_main_ttl=kdict.get("use", {}).get("main_ttl", default_main_ttl),
        )

    def __init__(
        self,
        wildcard: str,
        specific_retry_ttl: int = None,
        specific_main_ttl: int = None,
    ):
        self.wildcard = wildcard
        self.specific_retry_ttl = specific_retry_ttl
        self.specific_main_ttl = specific_main_ttl

    def info(self):
        return {
            "when_queue_contains": self.wildcard,
            "specific_retry_ttl": self.specific_retry_ttl,
            "specific_main_ttl": self.specific_main_ttl,
        }

    def has_specific_config(self, queue_name: str) -> bool:
        return fnmatch(queue_name, self.wildcard)

    def get_retry_ttl(self):
        return self.specific_retry_ttl

    def get_main_ttl(self):
        return self.specific_main_ttl
