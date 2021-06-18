def is_slack_available() -> bool:
    try:
        import slack  # noqa
    except (RuntimeError, ImportError):
        return False
    return True
