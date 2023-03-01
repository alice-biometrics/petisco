def is_redis_available() -> bool:
    try:
        import redis  # noqa
    except (RuntimeError, ImportError):
        return False
    return True
