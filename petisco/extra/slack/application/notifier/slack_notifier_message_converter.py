from abc import abstractmethod
from typing import Dict, List, Union

from petisco.base.application.notifier.notifier_exception_message import (
    NotifierExceptionMessage,
)
from petisco.base.application.notifier.notifier_message import NotifierMessage
from petisco.base.misc.interface import Interface


class SlackNotifierMessageConverter(Interface):
    @abstractmethod
    def convert(
        self, notifier_message: Union[NotifierMessage, NotifierExceptionMessage]
    ) -> List[Dict]:
        """
        Should return a list of blocks. See: https://api.slack.com/reference/block-kit/blocks
        """
        raise NotImplementedError
