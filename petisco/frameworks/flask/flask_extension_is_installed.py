def flask_extension_is_installed() -> bool:
    try:
        import connexion  # noqa: F401

        return True
    except:  # noqa: E722
        return False
