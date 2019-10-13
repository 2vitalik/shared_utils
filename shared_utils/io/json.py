import json

from shared_utils.io.path import encoded_filename, ensure_parent_dir


@encoded_filename
def json_dump(filename, data):
    ensure_parent_dir(filename)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@encoded_filename
def json_load(filename):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)
