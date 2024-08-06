import time
import functools


def profiler(func):  # type: ignore
    """
    Returns profiling decorator, which counts calls of function
    and measure last function execution time.
    Results are stored as function attributes: `calls`, `last_time_taken`
    :param func: function to decorate
    :return: decorator, which wraps any function passed
    """
    calls = 0
    common_time = 0

    @functools.wraps(func)
    def wrapper(*args, **kwargs):  # type: ignore
        nonlocal common_time
        nonlocal calls
        calls = calls + 1
        # create local 'call' for every wrapper instance
        call = calls
        start_time = time.time()
        res = func(*args, **kwargs)
        common_time = time.time() - start_time
        wrapper.__dict__['calls'] = calls - call + 1
        wrapper.__dict__['last_time_taken'] = common_time
        return res

    return wrapper
