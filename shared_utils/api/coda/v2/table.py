
class CodaTable:
    def __init__(self, doc, table_id):
        self.doc = doc
        self.doc_id = doc.doc_id
        self.api = doc.api
        self.table_id = table_id
        self.url_prefix = f'docs/{self.doc_id}/tables/{table_id}'

        self.columns_cache = self.doc.cache.columns_cache[table_id]['columns']
        self.overridden = \
            self.doc.conf.overridden.get(table_id, {}).get('columns', {})
        self.customize = \
            self.doc.conf.overridden.get(table_id, {}).get('customize', {})
        self.columns = {
            column_id: self._get_column_name(column_id)
            for column_id in self.columns_cache.keys()
        }

    def _request(self, url_suffix, method, params=None):  # internal
        url = f'{self.url_prefix}/{url_suffix}'
        return self.api.request(url, method, params)

    def _items_request(self, url_suffix, params=None):  # internal
        url = f'{self.url_prefix}/{url_suffix}'
        return self.api.items_request(url, params)

    def fetch_columns(self):
        ...  # todo?

    def _get_column_name(self, column_id):  # internal
        return (
            self.overridden.get(column_id)
            or self.columns_cache.get(column_id, {}).get('name')
            or column_id
        )

    def _get_column_id(self, column):  # internal
        # try to use `overridden`
        for column_id, value in self.overridden.items():
            if value == column:
                return column_id

        # try to use `columns_cache`
        for column_id, value in self.columns_cache.items():
            if value['name'] == column:
                return column_id

        # otherwise it's perhaps just `column_id` already
        return column

    def _get_item_values(self, item):
        values = {}
        for column_id, value in item['values'].items():
            name = self._get_column_name(column_id)
            values[name] = value

        result = {
            '@id': item['id'],
            '@index': item['index'],
            '@display_name': item['name'],
            '@created_at': item['createdAt'],
            '@updated_at': item['updatedAt'],
        }
        result.update(values)
        return result

    def get(self, row_id):
        item = self._request(f'rows/{row_id}', 'get')
        return self._get_item_values(item)

    def all(self):  # todo: sortBy, valueFormat ?
        response = self._items_request('rows', {'limit': 500})
        return [self._get_item_values(item) for item in response]

    def filter(self, query):
        ...  # todo: query for `all`

    def insert(self, row):
        return self.extend([row])  # `insert` => `extend` with only one row

    def _get_row_cells(self, data):
        return {
            'cells': [
                {
                    'column': self._get_column_id(column),
                    'value': value,
                }
                for column, value in data.items()
            ]
        }

    def extend(self, rows):
        params = {
            'rows': [self._get_row_cells(row)
                     for row in rows]
        }
        return self._request(f'rows', 'post', params)

    def update(self, row_id, changes):
        params = {
            'row': self._get_row_cells(changes)
        }
        return self._request(f'rows/{row_id}', 'put', params)

    def remove(self, row_id):
        self._request(f'rows/{row_id}', 'delete')
