import pytest

from petisco.notifier.infrastructure.slack.slack_notifier_message_converter import (
    SlackNotifierMessageConverter,
)


@pytest.mark.integration
def test_should_convert_a_basic_notifier_message(
    given_any_basic_notifier_message, given_any_message
):
    converter = SlackNotifierMessageConverter()
    blocks = converter.convert(given_any_basic_notifier_message)
    assert len(blocks) == 1
    assert "text" in blocks[0].keys()
    assert given_any_message in blocks[0]["text"]["text"]


@pytest.mark.integration
def test_should_convert_a_notifier_message_with_info_id(
    given_any_notifier_message_with_info_id, given_any_message
):
    converter = SlackNotifierMessageConverter()
    blocks = converter.convert(given_any_notifier_message_with_info_id)
    assert len(blocks) == 3
    assert "information" in blocks[0]["text"]["text"]
    assert "Client" in blocks[0]["text"]["text"]
    assert "User" in blocks[0]["text"]["text"]
    assert "divider" in blocks[1].values()
    assert "text" in blocks[2].keys()
    assert given_any_message in blocks[2]["text"]["text"]


@pytest.mark.integration
def test_should_convert_a_complete_notifier_message(
    given_any_complete_notifier_message, given_any_message, given_any_title
):
    converter = SlackNotifierMessageConverter()
    blocks = converter.convert(given_any_complete_notifier_message)
    assert len(blocks) == 5
    assert "Petisco" in blocks[0]["text"]["text"]
    assert "Application" in blocks[0]["text"]["text"]
    assert "information" in blocks[1]["text"]["text"]
    assert "Client" in blocks[1]["text"]["text"]
    assert "User" in blocks[1]["text"]["text"]
    assert "divider" in blocks[2].values()
    assert "text" in blocks[3].keys()
    assert given_any_title in blocks[3]["text"]["text"]
    assert "text" in blocks[4].keys()
    assert given_any_message in blocks[4]["text"]["text"]


@pytest.mark.integration
def test_should_convert_a_notifier_exception_message(
    given_any_complete_notifier_exception_message,
    given_any_exception,
    given_any_traceback,
):
    converter = SlackNotifierMessageConverter()
    blocks = converter.convert(given_any_complete_notifier_exception_message)
    assert len(blocks) == 7
    assert "Petisco" in blocks[0]["text"]["text"]
    assert "Application" in blocks[0]["text"]["text"]
    assert "information" in blocks[1]["text"]["text"]
    assert "Client" in blocks[1]["text"]["text"]
    assert "User" in blocks[1]["text"]["text"]
    assert "divider" in blocks[2].values()
    assert "text" in blocks[3].keys()
    assert str(given_any_exception) in blocks[3]["text"]["text"]
    assert "text" in blocks[4].keys()
    assert "Executor" in blocks[4]["text"]["text"]
    assert "text" in blocks[5].keys()
    assert "text" in blocks[6].keys()
    assert str(given_any_traceback) in blocks[6]["text"]["text"]


@pytest.mark.integration
def test_should_truncate_a_long_block_when_convert_slack_notifier(
    given_long_traceback_complete_notifier_exception_message,
):
    converter = SlackNotifierMessageConverter()
    blocks = converter.convert(given_long_traceback_complete_notifier_exception_message)
    assert "text" in blocks[5].keys()
    assert len(blocks[5]["text"]["text"]) < 3000
