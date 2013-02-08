import json

from model import Project, Category, Task

class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Project):
            return {'class': obj.__class__.__name__, 'id': obj.id, 'name': obj.name, 'default': obj.default}
        if isinstance(obj, Category):
            return {'class': obj.__class__.__name__, 'id': obj.id, 'name': obj.name, 'project_id': obj.project_id}
        if isinstance(obj, Task):
            return {'class': obj.__class__.__name__, 'id': obj.id, 'name': obj.name, 'category_id': obj.category_id, 'enabled': obj.enabled}

class ModelDecoder(json.JSONEncoder):
    pass

class JSon(Backend):
    def __init__(self, filename):
        self.filename = filename
        f = open(filename, 'r')
        str = f.read()
        f.close()
        items = json.load(f, cls=ModelEncoder)
        for item in items:
            self.data[item.id] = item

    def close(self):
        pass

    def commit(self):
        str = json.dumps(self.data, cls=ModelDecoder)
        f = open(self.filename, 'w')
        f.write(str)
        f.close()

    def create(self):
        f = open(self.filename, 'a')
        f.close()

    def drop(self):
        f = open(self.filename, 'w')
        f.close()

    def reset(self):
        pass

    def apply_flter(self, query, flt):
        pass

    def item_exists(self, cls, flt = None):
        pass

    def add_item(self, item):
        pass

    def delete_item(self, item):
        pass

    def update_item(self, item):
        pass

    def get_first_item(self, cls):
        pass

    def get_items(self, cls, flt = None):
        pass

    def get_item(self, cls, flt = None):
        pass

    def bulk_update(self, cls, changes, flt = None):
        pass
