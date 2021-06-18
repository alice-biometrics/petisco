def is_fastapi_available() -> bool:
    try:
        import fastapi  # noqa
    except (RuntimeError, ImportError):
        return False
    return True
