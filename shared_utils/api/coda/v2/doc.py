from os.path import join, exists

from shared_utils.api.coda.v2.api import CodaApi
from shared_utils.api.coda.v2.doc_cache import CodaDocCache
from shared_utils.api.coda.v2.doc_conf import CodaDocConf
from shared_utils.api.coda.v2.table import CodaTable
from shared_utils.io.yamls import load_yaml, dump_yaml


class CodaDoc:
    def __init__(self, doc_id, coda_api=None, coda_token=None,
                 conf_path='coda_conf'):
        # process with `doc_id`:
        if doc_id[0] != 'd':
            raise RuntimeError(f'Wrong doc_id: "{doc_id}"')
        self.doc_id = doc_id[1:]

        # process with CodaApi:
        if coda_api:
            self.api = coda_api
        elif coda_token:
            self.api = CodaApi(coda_token, conf_path)
        else:
            msg = f'Either `coda_api` or `coda_token` should be set'
            raise RuntimeError(msg)

        self.cache = CodaDocCache(self)
        self.conf = CodaDocConf(self)

        # process with `tables`:
        self.tables = {
            self._table_name(table_id): CodaTable(self, table_id)
            for table_id in self.cache.table_cache
        }

    def update_structure(self):
        self.cache.update_cache()
        self.conf.update_original()

    def items_request(self, url_suffix):
        return self.api.items_request(f'docs/{self.doc_id}/{url_suffix}')

    def _table_name(self, table_id):
        original_name = self.cache.table_cache[table_id]

        if table_id in self.conf.overridden:
            return self.conf.overridden[table_id].get('name', original_name)

        return original_name

    def __getattr__(self, table_name):
        if table_name not in self.tables:
            raise AttributeError(f"Table `{table_name}` not found.")

        return self.tables[table_name]
