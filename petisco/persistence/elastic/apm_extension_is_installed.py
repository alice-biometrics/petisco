def apm_extension_is_installed() -> bool:
    try:
        import elasticapm  # noqa: F401

        return True
    except ModuleNotFoundError:
        return False
