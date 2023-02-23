
class Item:
    def __init__(self, api, node_id, name, desc, complete, modified,
                 sub_lists):
        self.api = api
        self.node_id = node_id
        self.name = str(name)
        self.desc = desc
        self.complete = complete
        self.modified = modified
        self.sub_lists = sub_lists

    def __getitem__(self, index):
        if type(index) == int:
            return self.sub_lists[index]

        if type(index) == str:
            for child in self.sub_lists:
                if child.name == index:
                    return child
            raise ValueError(f'Element "{index}" not found')

        raise TypeError('Wrong type for index')

    def __iter__(self):
        yield from self.sub_lists

    @property
    def count(self):
        return len(self.sub_lists)

    def append(self, name, desc='', priority=None):
        new_node_id = self.api.create_node(self.node_id, str(name), desc,
                                           priority or 999)

        item = Item(self.api, new_node_id, name, desc, False, '?', [])
        if priority:
            self.sub_lists.insert(priority, item)
        else:
            self.sub_lists.append(item)
        return item

    def remove(self):
        self.api.remove_node(self.node_id)
