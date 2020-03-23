import time


def timer(func):
    def _timer(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)

        elapsed_time = time.time() - start_time

        return result, elapsed_time

    return _timer
