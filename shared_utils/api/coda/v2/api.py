import time

import requests
from requests.exceptions import ConnectionError, HTTPError


class CodaApi:
    def __init__(self, coda_token, cache_path='coda_cache', conf_path=None):
        self.coda_token = coda_token  # todo: try to make it class attribute?
        self.cache_path = cache_path
        self.conf_path = conf_path

    def raw_request(self, url, method, headers, params):
        if method == 'get':
            return requests.get(url, headers=headers, params=params)
        elif method == 'post':
            return requests.post(url, headers=headers, json=params)
        elif method == 'put':
            return requests.put(url, headers=headers, json=params)
        elif method == 'delete':
            return requests.delete(url, headers=headers, json=params)
        else:
            raise NotImplementedError()

    def try_request(self, *args, **kwargs):
        try:
            response = self.raw_request(*args, **kwargs)
        except ConnectionError:
            ...  # todo: something?
            raise
        try:
            response.raise_for_status()  # Throw if there was an error (1)
        except HTTPError:
            ...  # todo: slack_error ?

            time.sleep(1)
            # make another attempt:
            response = self.raw_request(*args, **kwargs)
            try:
                response.raise_for_status()  # Throw if there was an error (2)
            except HTTPError:
                print(response.content)
                ...  # todo: slack_error ?
                raise
        return response

    def request(self, url, method='get', params=None):
        # url:
        if not url.startswith('https://'):
            url = f'https://coda.io/apis/v1/{url}'
        print(f'Request({method}): {url}')

        # headers:
        headers = {'Authorization': f'Bearer {self.coda_token}'}

        # _request:
        response = self.try_request(url, method, headers, params)
        return response.json()

    def items_request(self, url, payload=None):
        response = self.request(url, 'get', payload)
        items = response['items']
        while 'nextPageLink' in response:
            next_link = response.get('nextPageLink')
            response = self.request(next_link)
            items.extend(response['items'])
        return items
