def is_pika_available() -> bool:
    try:
        import pika  # noqa
    except (RuntimeError, ImportError):
        return False
    return True
