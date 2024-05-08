from random import random

from petisco.base.application.chaos.chaos_config import chaos_config


class ChaosInvalidMessagePublication(Exception): ...


def check_chaos_publication():
    value = random()
    if value < chaos_config.percentage_invalid_message_publication:
        raise ChaosInvalidMessagePublication()
