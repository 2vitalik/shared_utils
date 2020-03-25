from os.path import join

from shared_utils.io.lock.lock_file import lock_file, unlock_file


def locked(slug, path='.'):
    def decorator(func):
        def wrapped(*args, **kwargs):
            lock_path = join(path, slug)
            lock_file(lock_path)
            try:
                return func(*args, **kwargs)
            finally:
                unlock_file(lock_path)
        return wrapped
    return decorator
