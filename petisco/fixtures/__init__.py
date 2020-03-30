try:
    from .fixtures import *  # noqa F403
except (RuntimeError, ImportError):
    print(
        "Impossible to import fixtures. fixtures petisco extra is required, install it with `pip install petisco[fixtures]`"
    )
