def is_sqlalchemy_available() -> bool:
    try:
        import sqlalchemy  # noqa
    except (RuntimeError, ImportError):
        return False
    return True
