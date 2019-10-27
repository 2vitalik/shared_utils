import json
import logging

import requests

from shared_utils.conf import conf


def post_to_slack(chat, message, emoji=None):
    if conf.slack_disabled:
        return
    url = conf.slack_hooks.get(chat)
    if not url:
        return
    if emoji:
        message = f':{emoji}: {message}'
    payload = {"text": message}
    headers = {'content-type': 'application/json'}
    requests.post(url, data=json.dumps(payload), headers=headers)
