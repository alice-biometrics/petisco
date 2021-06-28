def is_elastic_available() -> bool:
    try:
        import elasticsearch  # noqa
    except (RuntimeError, ImportError):
        return False
    return True
