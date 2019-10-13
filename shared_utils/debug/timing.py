import functools
from datetime import datetime

from shared_utils.conf import conf


def timing(func=None, *, desc=None, skip_desc=None, prefix=None, suffix=None,
           skip_milliseconds=None):
    """Measures time spent for function."""

    if func is None:
        return lambda f: timing(f, desc=desc, skip_desc=skip_desc,
                                prefix=prefix, suffix=suffix,
                                skip_milliseconds=skip_milliseconds)

    skip_desc = skip_desc or conf.timing_skip_desc
    prefix = prefix or conf.timing_prefix
    suffix = suffix or conf.timing_suffix
    skip_milliseconds = skip_milliseconds or conf.timing_skip_milliseconds

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        started_at = datetime.now()
        result = func(*args, **kwargs)
        delta = datetime.now() - started_at
        if skip_milliseconds:
            delta = str(delta).split('.')[0]

        output = f'{prefix} {delta}'
        if not skip_desc:
            output += f' {desc or func.__name__}'
        if suffix:
            output += suffix
        print(output)

        return result
    return wrapper
