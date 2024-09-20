import sys

collect_ignore = []

if sys.version_info < (3, 10):
    collect_ignore.append(
        "tests/modules/extra/threading/integration/test_concurrent_futures_pool_executor.py"
    )
