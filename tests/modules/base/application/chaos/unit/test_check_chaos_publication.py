from unittest.mock import patch

import pytest
from pydantic import ValidationError

from petisco.base.application.chaos.chaos_config import ChaosConfig, chaos_config
from petisco.base.application.chaos.check_chaos import (
    ChaosInvalidMessagePublication,
    check_chaos_publication,
)


@pytest.mark.unit
class TestCheckChaosPublication:
    def should_construct_chaos_config_with_envar_modifications(self, monkeypatch):
        monkeypatch.setenv("PETISCO_CHAOS_PERCENTAGE_INVALID_MESSAGE_PUBLICATION", "0.1")
        monkeypatch.setenv("PETISCO_CHAOS_PERCENTAGE_SIMULATE_NACK", "0.2")
        monkeypatch.setenv("PETISCO_CHAOS_DELAY_AFTER_MESSAGE_CONSUME_SECONDS", "0.3")
        monkeypatch.setenv("PETISCO_CHAOS_PERCENTAGE_SIMULATE_FAILURES", "0.4")
        monkeypatch.setenv("PETISCO_CHAOS_PROTECTED_ROUTING_KEYS", "petisco.routing_key")

        chaos_config = ChaosConfig()

        assert chaos_config.percentage_invalid_message_publication == 0.1
        assert chaos_config.percentage_simulate_nack == 0.2
        assert chaos_config.delay_after_message_consume_seconds == 0.3
        assert chaos_config.percentage_simulate_failures == 0.4
        assert chaos_config.protected_routing_keys == "petisco.routing_key"

    @pytest.mark.parametrize(
        "env,value",
        [
            ("PETISCO_CHAOS_PERCENTAGE_INVALID_MESSAGE_PUBLICATION", "100.0"),
            ("PETISCO_CHAOS_PERCENTAGE_SIMULATE_NACK", "100.0"),
            ("PETISCO_CHAOS_DELAY_AFTER_MESSAGE_CONSUME_SECONDS", "100.0"),
            ("PETISCO_CHAOS_PERCENTAGE_SIMULATE_FAILURES", "100.0"),
        ],
    )
    def should_raise_if_construct_chaos_config_with_invalid_percentage_invalid_message_publication(
        self, monkeypatch, env, value
    ):
        monkeypatch.setenv(env, value)
        with pytest.raises(ValidationError):
            ChaosConfig()

    def should_check_chaos_publication_without_raising_error(self):  # noqa
        check_chaos_publication()

    def should_check_chaos_publication_raising_error(self):  # noqa
        with patch.object(chaos_config, "percentage_invalid_message_publication", 1.0), pytest.raises(
            ChaosInvalidMessagePublication
        ):
            check_chaos_publication()
