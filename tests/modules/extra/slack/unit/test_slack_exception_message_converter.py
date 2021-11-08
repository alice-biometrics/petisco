import pytest

from petisco.extra.slack import ExceptionBlocksSlackNotifierMessageConverter
from tests.modules.extra.slack.mother.notifier_exception_message_mother import (
    NotifierExceptionMessageMother,
)


@pytest.mark.unit
def test_exception_blocks_slack_converter_should_convert_a_notifier_exception_message():
    converter = ExceptionBlocksSlackNotifierMessageConverter()
    notifier_exception_message = NotifierExceptionMessageMother.any()
    blocks = converter.convert(notifier_exception_message)
    block_contents = [block["text"]["text"] for block in blocks if block.get("text")]
    content = "".join(block_contents)
    assert notifier_exception_message.title in content
    assert notifier_exception_message.executor in content
    assert str(notifier_exception_message.exception) in content
    assert notifier_exception_message.traceback in content


@pytest.mark.unit
def test_exception_blocks_slack_converter_should_truncate_long_blocks_when_convert_slack_notifier():
    converter = ExceptionBlocksSlackNotifierMessageConverter()
    notifier_exception_message = NotifierExceptionMessageMother.long()
    blocks = converter.convert(notifier_exception_message)
    block_contents = [block["text"]["text"] for block in blocks if block.get("text")]
    assert len("".join(block_contents)) < 3000
