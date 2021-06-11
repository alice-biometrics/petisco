from abc import abstractmethod
from typing import List, Dict

from petisco.base.util.interface import Interface
from petisco.legacy.notifier.domain.notifier_message import NotifierMessage


class SlackNotifierMessageConverter(Interface):
    @abstractmethod
    def convert(self, notifier_message: NotifierMessage) -> List[Dict]:
        """
        Should return a list of blocks. See: https://api.slack.com/reference/block-kit/blocks
        """
        raise NotImplementedError
