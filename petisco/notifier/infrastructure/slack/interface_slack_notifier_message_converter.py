from abc import ABCMeta, abstractmethod
from typing import List, Dict

from petisco.notifier.domain.notifier_message import NotifierMessage


class ISlackNotifierMessageConverter:

    __metaclass__ = ABCMeta

    def __repr__(self):
        return f"ISlackMessageConverter"

    @abstractmethod
    def convert(self, notifier_message: NotifierMessage) -> List[Dict]:
        """
        Should return a list of blocks. See: https://api.slack.com/reference/block-kit/blocks
        """
        raise NotImplementedError
