import traceback
from os.path import join

from shared_utils.common.dt import dt, dtf
from shared_utils.conf.conf import conf
from shared_utils.io.io import append
from shared_utils.io.path import ensure_parent_dir


def log_status(cron_key, line):
    log_day('status', f'<{cron_key}>  {line}')


def log(filename, line, path=conf.logs_path):
    if path:
        filename = join(path, filename)
    ensure_parent_dir(filename)
    append(filename, f'{dt()}: {line}')


def log_day(slug, value, path=conf.logs_path):
    log(f"{slug}/{dtf('Ym/Ymd')}.txt", value, path=path)


def log_hour(slug, value, path=conf.logs_path):
    log(f"{slug}/{dtf('Ym/dh')}.txt", value, path=path)


def log_exception(slug):
    def decorator(func):
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log(f"exceptions/{slug}/{dtf('Ym/Ymd')}.txt",
                    traceback.format_exc(), path=conf.logs_path)
                # todo: send email or/and telegram message !!
                raise
        return wrapped
    return decorator
