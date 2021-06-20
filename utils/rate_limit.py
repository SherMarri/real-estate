from datetime import datetime, timedelta
import time
from functools import wraps


def rate_limit(*args, **kwargs):
    """
    Apply a rate limit so that we're not calling Zameen.com too frequently, \
        which helps avoid captchas and also ensure's we're good API-using citizens
    """

    func = None
    if len(args) == 1 and callable(args[0]):
        func = args[0]

    if func:
        seconds = 5  # default values

    if not func:
        seconds = kwargs.get("seconds")
    
    def callable_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            result = func(*args, **kwargs)
            return result

        return wrapper

    return callable_func(func) if func else callable_func
