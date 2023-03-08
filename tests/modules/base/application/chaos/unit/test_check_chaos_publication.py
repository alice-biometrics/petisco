from unittest.mock import patch

import pytest

from petisco.base.application.chaos.chaos_config import chaos_config
from petisco.base.application.chaos.check_chaos import (
    ChaosInvalidMessagePublication,
    check_chaos_publication,
)


@pytest.mark.unit
class TestCheckChaosPublication:
    def should_check_chaos_publication_without_raising_error(self):  # noqa
        check_chaos_publication()

    def should_check_chaos_publication_raising_error(self):  # noqa
        with patch.object(chaos_config, "percentage_invalid_message_publication", 1.0):
            with pytest.raises(ChaosInvalidMessagePublication):
                check_chaos_publication()
