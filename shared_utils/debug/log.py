import traceback
from os.path import join

from shared_utils.common.dt import dt, dtf
from shared_utils.conf import conf
from shared_utils.io.io import append
from shared_utils.io.path import ensure_parent_dir


def log(filename, line, path=None):
    if path:
        filename = join(path, filename)
    ensure_parent_dir(filename)
    append(filename, f'{dt()}: {line}')


def log_day(slug, value, path=None):
    log(f"{slug}/{dtf('Ym/Ymd')}.txt", value, path=path)


def log_hour(slug, value, path=None):
    log(f"{slug}/{dtf('Ym/dh')}.txt", value, path=path)


def log_exception(slug):
    def decorator(func):
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log(f"exceptions/{slug}/{dtf('Ym/Ymd')}.txt",
                    traceback.format_exc(), path=conf.logs_path)
                raise
        return wrapped
    return decorator
