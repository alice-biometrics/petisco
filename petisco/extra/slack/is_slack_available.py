def is_slack_available() -> bool:
    try:
        import slack_sdk  # noqa
    except (RuntimeError, ImportError):
        return False
    return True
