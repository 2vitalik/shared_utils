import os
from os.path import join, exists

from shared_utils.common.dt import dt
from shared_utils.io.io import write


def locked_repeat(slug):
    def decorator(func):
        def wrapped(*args, **kwargs):
            lock_file = join(conf.ROOT_PATH, 'sys', 'lock', slug)
            if exists(lock_file):
                print(dt(), f'Already locked: `{slug}`')
                return
            write(lock_file, '')
            try:
                return func(*args, **kwargs)
            finally:
                os.remove(lock_file)
        return wrapped
    return decorator
