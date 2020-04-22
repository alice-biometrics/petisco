try:
    from .domain import *  # noqa F403
    from .application import *  # noqa F403
    from .persistence import *  # noqa F403
    from .client import *  # noqa F403
except (RuntimeError, ImportError):
    print(
        "Impossible to import fixtures. fixtures petisco extra is required, install it with `pip install petisco[fixtures]`"
    )
