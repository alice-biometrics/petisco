import sys
from typing import Union

from pydantic import Field
from pydantic_settings import BaseSettings

if sys.version_info >= (3, 9):
    from typing import Annotated  # noqa

    # Prepared for Pydantic 3.0
    class ChaosConfig(BaseSettings):
        percentage_invalid_message_publication: Annotated[float, Field(ge=0.0, le=1.0)] = Field(
            default=0.0,
            validation_alias="PETISCO_CHAOS_PERCENTAGE_INVALID_MESSAGE_PUBLICATION",
            description="Percentage of invalid message publication. Where 1.0 means rejecting all the publishing messages.",
        )
        percentage_simulate_nack: Annotated[float, Field(ge=0.0, le=1.0)] = Field(
            default=0.0,
            validation_alias="PETISCO_CHAOS_PERCENTAGE_SIMULATE_NACK",
            description="Percentage of simulate nack. Where 1.0 rejects all the consuming messages",
        )
        delay_after_message_consume_seconds: Annotated[float, Field(ge=0.0, le=60.0)] = Field(
            default=0.0,
            validation_alias="PETISCO_CHAOS_DELAY_AFTER_MESSAGE_CONSUME_SECONDS",
            description="Delay message handler execution for a given number of seconds",
        )
        percentage_simulate_failures: Annotated[float, Field(ge=0.0, le=1.0)] = Field(
            default=0.0,
            validation_alias="PETISCO_CHAOS_PERCENTAGE_SIMULATE_FAILURES",
            description="Percentage of simulate failures. Where 1.0 simulate always a failure on handlers",
        )
        protected_routing_keys: Union[str, None] = Field(
            default=None,
            validation_alias="PETISCO_CHAOS_PROTECTED_ROUTING_KEYS",
            description="Routing keys where chaos will not be applied",
        )
else:
    # Use deprecated confloat to support Python 3.8 (not available Annotated)
    from pydantic import confloat  # noqa

    class ChaosConfig(BaseSettings):
        percentage_invalid_message_publication: confloat(ge=0.0, le=1.0) = Field(
            default=0.0,
            validation_alias="PETISCO_CHAOS_PERCENTAGE_INVALID_MESSAGE_PUBLICATION",
            description="Percentage of invalid message publication. Where 1.0 means rejecting all the publishing messages.",
        )
        percentage_simulate_nack: confloat(ge=0.0, le=1.0) = Field(
            default=0.0,
            validation_alias="PETISCO_CHAOS_PERCENTAGE_SIMULATE_NACK",
            description="Percentage of simulate nack. Where 1.0 rejects all the consuming messages",
        )
        delay_after_message_consume_seconds: confloat(ge=0.0, le=60.0) = Field(
            default=0.0,
            validation_alias="PETISCO_CHAOS_DELAY_AFTER_MESSAGE_CONSUME_SECONDS",
            description="Delay message handler execution for a given number of seconds",
        )
        percentage_simulate_failures: confloat(ge=0.0, le=1.0) = Field(
            default=0.0,
            validation_alias="PETISCO_CHAOS_PERCENTAGE_SIMULATE_FAILURES",
            description="Percentage of simulate failures. Where 1.0 simulate always a failure on handlers",
        )
        protected_routing_keys: Union[str, None] = Field(
            default=None,
            validation_alias="PETISCO_CHAOS_PROTECTED_ROUTING_KEYS",
            description="Routing keys where chaos will not be applied",
        )


chaos_config = ChaosConfig()
