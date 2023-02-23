import json
import os
import uuid
from os.path import exists

from requests import Session

from shared_utils.api.workflowy.interface import Item
from shared_utils.io.json import json_load, json_dump


class WorkflowyAPI:
    def __init__(self, username, password, filename):
        self.logged_in = False
        self.username = username
        self.password = password
        self.filename = filename

        self.session = Session()
        self.client_id = None
        self.recent_transaction = None
        self.date_joined = None

        self.parents = {}
        self.sub_lists = {}

    def login_request(self, username, password):
        self.session.post("https://workflowy.com/ajax_login", data={
            'username': username,
            'password': password,
        })  # todo: get and return sessionid?

    def api_request(self, method, data=None):  # ok?
        if not self.logged_in:
            self.login_request(self.username, self.password)

        res = self.session.post(f"https://workflowy.com/{method}", data)
        all_data = json.loads(res.content)

        if 'projectTreeData' in all_data:
            main_info = all_data['projectTreeData']['mainProjectTreeInfo']

            # fixme: this is unsuccessful attempts with shared projects
            # main_info = \
            #     all_data['projectTreeData']['auxiliaryProjectTreeInfos'][0]

            if 'initialMostRecentOperationTransactionId' in main_info:
                self.recent_transaction = \
                    main_info['initialMostRecentOperationTransactionId']
                self.client_id = all_data['projectTreeData']['clientId']

        elif 'results' in all_data:
            result = all_data['results'][0]
            if 'new_most_recent_operation_transaction_id' in result:
                self.recent_transaction = \
                    result['new_most_recent_operation_transaction_id']
            if 'error' in result:
                raise Exception('Error in Workflowy API request')

        return all_data

    def load_all_data(self):
        if not exists(self.filename):
            return None
        return json_load(self.filename)

    def fetch_all_data(self):
        all_data = self.api_request('get_initialization_data')
        json_dump(self.filename, all_data)
        return all_data

    def get_all_data(self):
        all_data = self.load_all_data() or self.fetch_all_data()
        # print(json.dumps(all_data))  # fixme: just for debug

        main_info = all_data['projectTreeData']['mainProjectTreeInfo']

        # fixme: this is unsuccessful attempts with shared projects
        # main_info = \
        #     all_data['projectTreeData']['auxiliaryProjectTreeInfos'][0]

        raw_lists = []
        if 'rootProjectChildren' in main_info:
            raw_lists = main_info['rootProjectChildren']
        if 'dateJoinedTimestampInSeconds' in main_info:
            self.date_joined = main_info['dateJoinedTimestampInSeconds']
        self.parents = {}
        self.sub_lists = {}
        return self.parse_list({
            'id': 'None',
            # 'nm': None,
            # 'no': None,
            # 'cp': None,
            'lm': 0,
            'ch': raw_lists,
        }, False)

    def parse_list(self, raw_list, parent_id):  # recursive function
        node_id = raw_list['id'] if 'id' in raw_list else ''
        name = raw_list['nm'] if 'nm' in raw_list else ''
        description = raw_list['no'] if 'no' in raw_list else ''
        raw_sub_lists = raw_list['ch'] if 'ch' in raw_list else []
        complete = self.date_joined + raw_list['cp'] if 'cp' in raw_list else 0
        modified = self.date_joined + raw_list['lm'] if 'lm' in raw_list else 0
        sub_lists = []
        for raw_sub_list in raw_sub_lists:
            sub_lists.append(self.parse_list(raw_sub_list, node_id))
        sub_list = Item(self, node_id, name, description, complete, modified,
                        sub_lists)
        if parent_id:
            self.parents[node_id] = parent_id
        self.sub_lists[node_id] = sub_list
        return sub_list

    def request(self, action, data):
        self.api_request('push_and_poll', data={
            'client_id': self.client_id,
            'client_version': 18,
            'push_poll_id': 'HXRGpuXA',  # todo: make this dynamic?
            'push_poll_data': json.dumps([{
                'most_recent_operation_transaction_id': self.recent_transaction,
                'operations': [{
                    'type': action,
                    'data': data,
                }],
            }])
        })

    def create_node(self, parent_id, name, description, priority):
        new_id = str(uuid.UUID(bytes=os.urandom(16)))
        # todo: check if such entry already exists?
        self.request('create', {
            'projectid': new_id,
            'parentid': parent_id,
            'priority': priority,
        })
        self.request('edit', {
            'projectid': new_id,
            'name': name,
        })
        self.request('edit', {
            'projectid': new_id,
            'description': description,
        })
        return new_id

    def remove_node(self, node_id):
        self.request('delete', {
            'projectid': node_id,
        })
