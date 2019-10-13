import os
from os.path import exists

from common.dt import dt
from io.io import write
from io.path import encoded_filename
from io.lock.exceptions import LockError, UnlockError


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
