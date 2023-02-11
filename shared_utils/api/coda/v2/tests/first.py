import json

from shared_utils.api.coda.v2.doc import CodaDoc
from shared_utils.conf import conf


def pprint(json_data):
    print(json.dumps(json_data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    doc = CodaDoc('dBPqqG0xD2g', coda_token=conf.coda_token,
                  conf_path='coda_conf')

    # If we need to load new doc structure from coda:
    # doc.update_structure()

    # if we need to create `overriden.yaml`
    # doc.conf.create_overriden()

    # Before setting `overriden.yaml`:
    # pprint(doc.tables['Приоритеты'].all())

    # After setting `overriden.yaml`:
    pprint(doc.priorities.all())
