import meiga

if meiga.__version__ < "1.9.4":
    from meiga.on_failure_exception import (  # noqa
        OnFailureException as WaitingForEarlyReturn,
    )
elif meiga.__version__ == "1.9.4":
    from meiga.failures import WaitingForEarlyReturn  # noqa
else:
    from meiga import WaitingForEarlyReturn  # noqa
