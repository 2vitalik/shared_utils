import os
import time
from contextlib import contextmanager
from os.path import exists

from shared_utils.common.dt import dt
from shared_utils.io.io import write
from shared_utils.io.path import encoded_filename
from shared_utils.io.lock.exceptions import LockError, UnlockError


@encoded_filename
def is_locked(filename):
    return exists(filename + b'.lock')


@encoded_filename
def lock_file(filename):  # todo: возможно попробовать сделать context manager `with locked(...):`
    if is_locked(filename):
        raise LockError(filename)
    write(filename + b'.lock', dt())


@encoded_filename
def unlock_file(filename):
    if not is_locked(filename):
        raise UnlockError(filename)
    os.remove(filename + b'.lock')


@contextmanager
def locked_file(filename, attempts=1):
    interval = 0.1
    for attempt in range(attempts):
        try:
            lock_file(filename)
            break  # successfully locked file
        except LockError:
            time.sleep(interval)
            interval *= 2
    else:  # file was already locked during all attempts
        raise LockError(filename)

    try:
        yield  # go inside context manager body here
    finally:
        unlock_file(filename)
