from os.path import join, exists

from shared_utils.api.coda.v2.api import CodaApi
from shared_utils.api.coda.v2.doc_cache import CodaDocCache
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
        self.cache = CodaDocCache(self)

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
            for table_id in self.cache.table_cache
        }

    def list_request(self, url_suffix):
        return self.api.list_request(f'docs/{self.doc_id}/{url_suffix}')

    def save_original_conf(self):
        original_conf = {}

        for table_id, table_data in self.cache.columns_cache.items():
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
        return self.cache.table_cache[table_id]

    def __getattr__(self, table_name):
        if table_name in self.tables:
            return self.tables[table_name]
        raise AttributeError()
