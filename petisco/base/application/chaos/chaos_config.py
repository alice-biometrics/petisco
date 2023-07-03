from typing import Union

from pydantic import Field, confloat
from pydantic_settings import BaseSettings


class ChaosConfig(BaseSettings):
    percentage_invalid_message_publication: confloat(ge=0.0, le=1.0) = Field(
        default=0,
        validation_alias="PETISCO_CHAOS_PERCENTAGE_INVALID_MESSAGE_PUBLICATION",
        description="Percentage of invalid message publication. Where 1.0 means rejecting all the publishing messages.",
    )
    percentage_simulate_nack: confloat(ge=0.0, le=1.0) = Field(
        default=0,
        validation_alias="PETISCO_CHAOS_PERCENTAGE_SIMULATE_NACK",
        description="Percentage of simulate nack. Where 1.0 rejects all the consuming messages",
    )
    delay_after_message_consume_seconds: confloat(ge=0.0, le=60.0) = Field(
        default=0,
        validation_alias="PETISCO_CHAOS_DELAY_AFTER_MESSAGE_CONSUME_SECONDS",
        description="Delay message handler execution for a given number of seconds",
    )
    percentage_simulate_failures: confloat(ge=0.0, le=1.0) = Field(
        default=0,
        validation_alias="PETISCO_CHAOS_DELAY_AFTER_OPERATION_SECONDS",
        description="Percentage of simulate failures. Where 1.0 simulate always a failure on handlers",
    )
    protected_routing_keys: Union[str, None] = Field(
        default=None,
        validation_alias="PETISCO_CHAOS_PROTECTED_ROUTING_KEYS",
        description="Routing keys where chaos will not be applied",
    )


chaos_config = ChaosConfig()
