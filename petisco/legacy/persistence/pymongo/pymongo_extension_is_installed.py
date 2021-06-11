def mongodb_extension_is_installed() -> bool:
    try:
        import pymongo  # noqa: F401

        return True
    except:  # noqa: E722
        return False
