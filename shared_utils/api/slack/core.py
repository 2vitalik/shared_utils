import json

import requests

from shared_utils.common.dt import dtf, dt
from shared_utils.conf import conf
from shared_utils.io.io import append


def post_to_slack(chat, message, emoji=None):
    if conf.slack_disabled:
        return False
    url = conf.slack_hooks.get(chat)
    if emoji:
        message = f':{emoji}: {message}'
    if conf.slack_path:
        path = f'{conf.slack_path}/{chat}/{dtf("Ym/Ymd")}.txt'
        append(path, f'[{dt()}] {message}')
    if url is None:  # if there is no such key
        return False
    if url == '':  # if key is equal to '' in a special way
        return True
    payload = {"text": message}
    headers = {'content-type': 'application/json'}
    requests.post(url, data=json.dumps(payload), headers=headers)
    return True
