from os.path import join, exists

from shared_utils.api.coda.v2.api import CodaApi
from shared_utils.api.coda.v2.table import CodaTable
from shared_utils.io.yamls import load_yaml, dump_yaml


class CodaDoc:
    def __init__(self, doc_id, coda_api=None, coda_token=None,
                 cache_path='coda_cache', conf_path=None):
        # process with `doc_id`:
        if doc_id[0] != 'd':
            raise RuntimeError(f'Wrong doc_id: "{doc_id}"')
        self.doc_id = doc_id[1:]

        # process with CodaApi:
        if coda_api:
            self.api = coda_api
        elif coda_token:
            self.api = CodaApi(coda_token, cache_path, conf_path)
        else:
            raise RuntimeError(f'Either `coda_api` or `coda_token` should be set')

        # process with caches:
        self.cache_path = join(self.api.cache_path, doc_id)

        self.tables_cache_filename = join(self.cache_path, 'tables.yaml')
        self.columns_cache_filename = join(self.cache_path, 'columns.yaml')

        self.table_cache = self.get_tables_cache()
        self.columns_cache = self.get_columns_cache()

        # process with conf overrides:
        self.overridden = {}
        if self.api.conf_path:
            self.conf_path = join(self.api.conf_path, doc_id)
            self.overridden_filename = join(self.conf_path, 'overridden.yaml')
            self.original_filename = join(self.conf_path, 'original.yaml')
            if exists(self.overridden_filename):
                self.overridden = load_yaml(self.overridden_filename)

        # todo: `titles` and `hidden` things for `coda_changes`?

        # process with `tables`:
        self.tables = {
            self.table_key(table_id): CodaTable(self, table_id)
            for table_id in self.table_cache
        }

    def list_request(self, url_suffix):
        return self.api.list_request(f'docs/{self.doc_id}/{url_suffix}')

    def get_tables_cache(self):
        if not exists(self.tables_cache_filename):
            self.fetch_tables()
        return load_yaml(self.tables_cache_filename)
        # todo: save historical changes?

    def fetch_tables(self):
        tables = {}

        tables_response = self.list_request(f'tables')
        for table_data in tables_response:
            if table_data['tableType'] != 'table':
                continue
            table_id = table_data['id']
            table_name = table_data['name']
            tables[table_id] = table_name

        dump_yaml(self.tables_cache_filename, tables)

    def get_columns_cache(self):
        if not exists(self.columns_cache_filename):
            self.fetch_columns()
        return load_yaml(self.columns_cache_filename)
        # todo: save historical changes?

    def fetch_columns(self):
        columns_cache = {}

        for table_id, table_name in self.table_cache.items():
            table_columns = {}

            columns_response = self.list_request(f'tables/{table_id}/columns')
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

        dump_yaml(self.columns_cache_filename, columns_cache)
        # todo: check if changed and save historical

    def save_original_conf(self):
        original_conf = {}

        for table_id, table_data in self.columns_cache.items():
            columns = {}
            for column_id, column_data in table_data['columns'].items():
                columns[column_id] = column_data['name']
            original_conf[table_id] = {
                'name': table_data['name'],
                'columns': columns,
            }

        dump_yaml(f'{self.original_filename}', original_conf)

    def table_key(self, table_id):
        if table_id in self.overridden:
            return self.overridden[table_id]['name']
        return self.table_cache[table_id]

    def __getattr__(self, table_name):
        if table_name in self.tables:
            return self.tables[table_name]
        raise AttributeError()
