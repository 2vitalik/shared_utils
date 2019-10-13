import sys
from os.path import exists

from shared_utils.io.path import encoded_filename, ensure_parent_dir


@encoded_filename
def read(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()


@encoded_filename
def read_lines(filename, ignore_absent=False):
    if ignore_absent and not exists(filename):
        # todo: также писать куда-нибудь в логи?
        print(f"[read_lines] File doesn't exist: {filename}", file=sys.stderr)
        return []
    return read(filename).split('\n')


@encoded_filename
def write(filename, content):
    ensure_parent_dir(filename)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


@encoded_filename
def write_lines(filename, lines):
    return write(filename, '\n'.join(lines))


@encoded_filename
def append(filename, line):
    ensure_parent_dir(filename)
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f'{line}\n')


def compare(filename1, filename2):
    return read(filename1) == read(filename2)
