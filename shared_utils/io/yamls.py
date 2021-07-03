import re

import yaml.reader

from shared_utils.io.path import ensure_parent_dir

yaml.reader.Reader.NON_PRINTABLE = re.compile(  # to enable emoji etc.
    '[^'
    '\x09\x0A\x0D'
    '\x20-\x7E'
    '\x85'
    '\xA0-\uD7FF'
    '\uE000-\uFFFD'
    '\U00010000-\U0010FFFF'
    ']'
)


def load_yaml(filename):
    return yaml.load(open(filename, encoding='utf-8'), Loader=yaml.BaseLoader)


def dump_yaml(filename, data):
    ensure_parent_dir(filename)
    return yaml.dump(data, open(filename, 'w', encoding='utf-8'),
                     allow_unicode=True, sort_keys=False)
