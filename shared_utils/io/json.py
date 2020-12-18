import json
from os.path import exists

from shared_utils.io.path import encoded_filename, ensure_parent_dir


def json_dumps(data):
    return json.dumps(data, indent=4, ensure_ascii=False)


@encoded_filename
def json_dump(filename, data):
    ensure_parent_dir(filename)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@encoded_filename
def json_load(filename):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)


@encoded_filename
def json_dump_changed(filename, data):
    old_data = json_dumps(json_load(filename) if exists(filename) else None)
    new_data = json_dumps(data)
    if old_data != new_data:
        json_dump(filename, data)
        return True
    return False
