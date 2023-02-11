from os.path import join, exists

from shared_utils.io.yamls import load_yaml, dump_yaml


class CodaDocConf:
    def __init__(self, coda_doc):
        self.doc = coda_doc

        self.overriden_path = \
            join(self.doc.api.conf_path, f'd{self.doc.doc_id}', 'conf')

        self.overridden_filename = join(self.overriden_path, 'overridden.yaml')
        self.original_filename = join(self.overriden_path, 'original.yaml')

        self.init_overriden()
        self.overridden = self.load_overriden()

        # todo: `titles` and `hidden` things for `coda_changes`?

    def update_original(self):
        original_conf = {}

        for table_id, table_data in self.doc.cache.columns_cache.items():
            columns = {}
            for column_id, column_data in table_data['columns'].items():
                columns[column_id] = column_data['name']
            original_conf[table_id] = {
                'name': table_data['name'],
                'columns': columns,
            }

        dump_yaml(self.original_filename, original_conf)
        return original_conf

    def init_overriden(self):
        original = self.update_original()

        if not exists(self.overridden_filename):
            dump_yaml(self.overridden_filename, original)

    def clear_overriden(self):
        original = self.update_original()
        dump_yaml(self.overridden_filename, original)

    def load_overriden(self):
        if not exists(self.overridden_filename):
            return {}

        return load_yaml(self.overridden_filename)
