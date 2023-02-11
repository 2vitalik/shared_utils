from os.path import join, exists

from shared_utils.io.yamls import load_yaml, dump_yaml


class CodaDocCache:
    def __init__(self, coda_doc):
        self.doc = coda_doc

        self.cache_path = \
            join(self.doc.api.conf_path, f'd{self.doc.doc_id}', 'cache')

        self.tables_cache_filename = join(self.cache_path, 'tables.yaml')
        self.columns_cache_filename = join(self.cache_path, 'columns.yaml')

        self.table_cache = None
        self.columns_cache = None
        self._init_cache()

    def _init_tables_cache(self):
        if not exists(self.tables_cache_filename):
            return self._update_tables_cache()

        return self._load_table_cache()

    def _update_tables_cache(self):
        tables_response = self.doc.items_request(f'tables')

        tables = {}
        for table_data in tables_response:
            if table_data['tableType'] != 'table':
                continue
            table_id = table_data['id']
            table_name = table_data['name']
            tables[table_id] = table_name

        # todo: check if changed and save also historical
        dump_yaml(self.tables_cache_filename, tables)
        return self._load_table_cache()

    def _init_columns_cache(self):
        if not exists(self.columns_cache_filename):
            return self._update_columns_cache()

        return self._load_columns_cache()

    def _update_columns_cache(self):
        columns_cache = {}

        for table_id, table_name in self.table_cache.items():
            columns_response = \
                self.doc.items_request(f'tables/{table_id}/columns')

            table_columns = {}
            for column_data in columns_response:
                column_id = column_data['id']
                table_columns[column_id] = {
                    'name': column_data['name'],
                    'format': column_data['format'],
                    'display': column_data.get('display', False),
                    'formula': column_data.get('formula'),
                    'default': column_data.get('defaultValue'),
                }

            columns_cache[table_id] = {
                'name': table_name,
                'columns': table_columns,
            }

        # todo: check if changed and save also historical
        dump_yaml(self.columns_cache_filename, columns_cache)
        return self._load_columns_cache()

    def _load_table_cache(self):
        return load_yaml(self.tables_cache_filename)

    def _load_columns_cache(self):
        return load_yaml(self.columns_cache_filename)

    def _init_cache(self):
        self.table_cache = self._init_tables_cache()
        self.columns_cache = self._init_columns_cache()

    def update_cache(self):
        self.table_cache = self._update_tables_cache()
        self.columns_cache = self._update_columns_cache()
