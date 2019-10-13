import os
from genericpath import exists
from os.path import dirname


def encoded_filename(func):
    def wrapped(*args, **kwargs):
        filename = args[0]
        if type(filename) == str:
            args = (filename.encode(), *args[1:])  # need for Cyrl in Linux etc.
        return func(*args, **kwargs)
    return wrapped


@encoded_filename
def ensure_dir(path):
    if not path:
        return
    if not exists(path):
        os.makedirs(path)


@encoded_filename
def ensure_parent_dir(filename):
    ensure_dir(dirname(filename))


def fix_path(path):
    return '/'.join(fix_filename(name) for name in path.split('/'))


def fix_filename(filename):
    if filename.lower() in ['con', 'nul']:
        filename += '{}'
    return filename.\
        replace('?', '{question}').\
        replace(':', '{colon}').\
        replace('/', '{slash}').\
        replace('"', '{quot}').\
        replace('|', '{pipe}').\
        replace('*', '{asterisk}').\
        replace('<', '{lt}').\
        replace('>', '{gt}')


def unfix_filename(filename):
    if filename.lower() in ['con{}', 'nul{}']:
        return filename[:-2]
    return filename.\
        replace('{question}', '?').\
        replace('{colon}', ':').\
        replace('{slash}', '/').\
        replace('{quot}', '"').\
        replace('{pipe}', '|').\
        replace('{asterisk}', '*').\
        replace('{lt}', '<').\
        replace('{gt}', '>')
