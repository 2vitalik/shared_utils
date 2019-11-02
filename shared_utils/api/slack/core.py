import json

import requests

from shared_utils.conf import conf


def post_to_slack(chat, message, emoji=None):
    if conf.slack_disabled:
        return False
    url = conf.slack_hooks.get(chat)
    if not url:
        return False
    if emoji:
        message = f':{emoji}: {message}'
    payload = {"text": message}
    headers = {'content-type': 'application/json'}
    requests.post(url, data=json.dumps(payload), headers=headers)
    return True
