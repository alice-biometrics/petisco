import pytest

from petisco.extra.slack import BlocksSlackNotifierMessageConverter
from tests.modules.extra.slack.mother.notifier_message_mother import (
    NotifierMessageMother,
)


@pytest.mark.unit
def test_blocks_slack_converter_should_convert_a_notifier_message():
    converter = BlocksSlackNotifierMessageConverter()
    notifier_message = NotifierMessageMother.any()
    blocks = converter.convert(notifier_message)
    block_contents = [block["text"]["text"] for block in blocks if block.get("text")]
    assert notifier_message.title in block_contents
    assert notifier_message.message in block_contents
