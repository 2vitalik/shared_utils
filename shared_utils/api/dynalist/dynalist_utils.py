import json
from pprint import pprint

import requests

from shared_utils.conf import conf


def request(url, **kwargs):
    url = f'https://dynalist.io/api/v1/{url}'
    data = {'token': conf.dynalist_token}
    data.update(kwargs)
    result = json.loads(requests.post(url, json=data).content)
    # pprint(result)  # for debug
    return result


def get_files():
    return request('file/list')


def get_file(file_id):
    return request('doc/read', file_id=file_id)


def get_nodes(file_id):
    nodes = {}
    data = get_file(file_id)
    for node in data['nodes']:
        nodes[node['id']] = node
    return nodes


def get_node(file_id, node_id):
    nodes = get_nodes(file_id)
    return nodes[node_id]['content']


def get_children(file_id, node_id):
    nodes = get_nodes(file_id)
    node = nodes[node_id]
    children = []
    for child_id in node['children']:
        children.append(nodes[child_id]['content'])
    return children


def insert_node(file_id, node_id, content):
    return request('doc/edit', file_id=file_id, changes=[{
        'action': 'insert',
        'parent_id': node_id,
        'content': content,
    }])


def change_node(file_id, node_id, content):
    return request('doc/edit', file_id=file_id, changes=[{
        'action': 'edit',
        'node_id': node_id,
        'content': content,
    }])


if __name__ == '__main__':
    pprint(get_files())
    # get_file('...')
    pass
