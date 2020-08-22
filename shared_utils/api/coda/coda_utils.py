import time
from pprint import pprint

import requests
from requests.exceptions import ConnectionError, HTTPError


def request(coda_token, url, payload=None, method='get'):
    if not url.startswith('https://'):
        url = f'https://coda.io/apis/v1/{url}'
    print(url)
    headers = {'Authorization': f'Bearer {coda_token}'}

    def make_request():
        if method == 'get':
            return requests.get(url, headers=headers)
        elif method == 'post':
            return requests.post(url, headers=headers, json=payload)
        elif method == 'put':
            return requests.put(url, headers=headers, json=payload)
        else:
            raise NotImplementedError()

    try:
        response = make_request()
    except ConnectionError:
        ...  # todo: something?
        raise
    try:
        response.raise_for_status()  # Throw if there was an error (1)
    except HTTPError:
        time.sleep(1)
        response = make_request()  # make another attempt
        try:
            response.raise_for_status()  # Throw if there was an error (2)
        except HTTPError:
            print(response.content)
            raise

    result = response.json()
    # pprint(result)  # for debug
    return result


def request_put(coda_token, url, payload):
    return request(coda_token, url, payload, 'put')


def request_post(coda_token, url, payload):
    return request(coda_token, url, payload, 'post')


def get_tables(coda_token, doc_id):
    return request(coda_token, f'docs/{doc_id}/tables')


def print_tables(coda_token, doc_id):
    tables = request(coda_token, f'docs/{doc_id}/tables')
    for table in tables['items']:
        print(table['id'], table['name'])


def get_columns(coda_token, doc_id, table_id):
    data = request(coda_token, f'docs/{doc_id}/tables/{table_id}/columns')
    next_link = data.get('nextPageLink')
    if next_link:
        next_data = get_next_columns(coda_token, next_link)
        data['items'].extend(next_data['items'])
    return data


def get_next_columns(coda_token, next_link):
    data = request(coda_token, next_link)
    next_next_link = data.get('nextPageLink')
    if next_next_link:
        next_data = get_next_columns(coda_token, next_next_link)
        data['items'].extend(next_data['items'])
    return data


def print_columns(coda_token, doc_id, table_id):
    columns = get_columns(coda_token, doc_id, table_id)
    for column in columns['items']:
        print(f"{column['name']}: {column['id']}")


def get_rows(coda_token, doc_id, table_id):
    data = request(coda_token, f'docs/{doc_id}/tables/{table_id}/rows')
    next_link = data.get('nextPageLink')
    if next_link:
        next_data = get_next_rows(coda_token, next_link)
        data['items'].extend(next_data['items'])
    return data


def get_next_rows(coda_token, next_link):
    data = request(coda_token, next_link)
    next_next_link = data.get('nextPageLink')
    if next_next_link:
        next_data = get_next_rows(coda_token, next_next_link)
        data['items'].extend(next_data['items'])
    return data


def get_rows_data(coda_token, doc_id, table_id, columns):
    results = []
    rows = get_rows(coda_token, doc_id, table_id)
    for row in rows['items']:
        entry = {
            'id': row['id'],
            # 'index': row['index'],
        }
        for col_name, col_id in columns.items():
            if not col_id or col_id in ['c-']:
                continue
            entry[col_name] = row['values'][col_id]
        results.append(entry)
    return results  # todo: sort by index?


def get_rows_dict(coda_token, doc_id, table_id, columns):
    results = {}
    rows = get_rows(coda_token, doc_id, table_id)
    for row in rows['items']:
        entry = {}
        for col_name, col_id in columns.items():
            if not col_id or col_id in ['c-']:
                continue
            entry[col_name] = row['values'][col_id]
        results[row['id']] = entry
    return results  # todo: sort by key?


def get_rows_data_by_yaml(coda_token, doc_id, table_info):
    return get_rows_data(coda_token, doc_id,
                         table_info['table_id'], table_info['columns'])


def get_rows_dict_by_yaml(coda_token, doc_id, table_info):
    return get_rows_dict(coda_token, doc_id,
                         table_info['table_id'], table_info['columns'])


def print_rows(coda_token, doc_id, table_id):
    rows = get_rows(coda_token, doc_id, table_id)
    pprint(rows)


def update_row(coda_token, doc_id, table_id, columns, row_id, data):
    url = f'docs/{doc_id}/tables/{table_id}/rows/{row_id}'
    payload = {
        'row': {
            'cells': [
                # {'column': '<column ID>',
                #  'value': 'Get groceries from Whole Foods'},
            ],
        },
    }
    for col_name, col_value in data.items():
        payload['row']['cells'].append({
            'column': columns[col_name],
            'value': col_value
        })
    return request_put(coda_token, url, payload)


def update_row_by_yaml(coda_token, doc_id, table_info, row_id, data):
    return update_row(coda_token, doc_id, table_info['table_id'],
                      table_info['columns'], row_id, data)


def append_row(coda_token, doc_id, table_id, columns, data):
    url = f'docs/{doc_id}/tables/{table_id}/rows'
    payload = {
        'rows': [
            {
                'cells': [
                    # {'column': '<column ID>',
                    #  'value': 'Get groceries from Whole Foods'},
                ],
            }
        ],
    }
    for col_name, col_value in data.items():
        payload['rows'][0]['cells'].append({
            'column': columns[col_name],
            'value': col_value
        })
    return request_post(coda_token, url, payload)


def append_row_by_yaml(coda_token, doc_id, table_info, data):
    return append_row(coda_token, doc_id, table_info['table_id'],
                      table_info['columns'], data)
