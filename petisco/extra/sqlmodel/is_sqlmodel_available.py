def is_sqlmodel_available() -> bool:
    try:
        import sqlmodel  # noqa
    except (RuntimeError, ImportError):
        return False
    return True
