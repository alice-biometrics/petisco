def flask_extension_is_installed() -> bool:
    try:
        import connexion

        return True
    except:
        return False
