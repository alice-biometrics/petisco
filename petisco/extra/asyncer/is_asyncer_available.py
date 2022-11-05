def is_asyncer_available() -> bool:
    try:
        import asyncer  # noqa
    except (RuntimeError, ImportError):
        return False
    return True
