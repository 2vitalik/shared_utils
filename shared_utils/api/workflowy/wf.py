from shared_utils.api.workflowy.api import WorkflowyAPI


class Workflowy:
    def __init__(self, username, password, filename):
        self.api = WorkflowyAPI(username, password, filename)
        self.root = self.api.get_all_data()
