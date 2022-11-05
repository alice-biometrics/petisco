from petisco.extra.asyncer.is_asyncer_available import is_asyncer_available

__all__ = []

if is_asyncer_available():
    from petisco.extra.asyncer.async_pool_executor import AsyncPoolExecutor

    __all__ = ["AsyncPoolExecutor"]
