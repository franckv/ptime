import json
import os

from model import Project, Category, Task
from . import Backend

class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Project):
            return {'class': obj.__class__.__name__, 'id': obj.id, 'name': obj.name, 'default': obj.default}
        if isinstance(obj, Category):
            return {'class': obj.__class__.__name__, 'id': obj.id, 'name': obj.name, 'project_id': obj.project_id}
        if isinstance(obj, Task):
            return {'class': obj.__class__.__name__, 'id': obj.id, 'name': obj.name, 'category_id': obj.category_id, 'enabled': obj.enabled, 'duration': obj.duration, 'completed': obj.completed, 'rating': obj.rating}

class ModelDecoder(json.JSONDecoder):
    def decode(self, s):
        items = []

        if s is None or len(s) == 0:
            return items

        data = json.JSONDecoder.decode(self, s)

        for obj in data:
            cls = obj['class']

            if cls == 'Project':
                o = Project(obj['name'])
                o.default = obj['default']
            elif cls == 'Category':
                o = Category(obj['name'])
                o.project_id = obj['project_id']
            elif cls == 'Task':
                o = Task(obj['name'])
                o.default = obj['enabled']
                o.category_id = obj['category_id']
                o.rating = obj['rating']
                o.completed = obj['completed']
                o.duration = obj['duration']
            o.id = obj['id']
            items.append(o)
        return items

class JSon(Backend):
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        Project.last_id = 0
        Category.last_id = 0
        Task.last_id = 0

        if os.path.exists(filename):
            f = open(filename, 'r')
            items = json.load(f, cls=ModelDecoder)
            f.close()
            for item in items:
                if item.id > item.__class__.last_id:
                    item.__class__.last_id = item.id
                key = item.__class__.__name__ + '.' + str(item.id)
                self.data[key] = item

    def close(self):
        pass

    def commit(self):
        s = json.dumps(self.data.values(), cls=ModelEncoder, separators=(',', ':'))
        f = open(self.filename, 'w')
        f.write(s)
        f.close()

    def create(self):
        f = open(self.filename, 'a')
        f.close()

    def drop(self):
        self.reset()

    def reset(self):
        self.data = {}
        Project.last_id = 0
        Category.last_id = 0
        Task.last_id = 0

        f = open(self.filename, 'w')
        f.close()

    def item_exists(self, cls, flt = None):
        return self.get_item(cls, flt) is not None

    def add_item(self, item):
        if not hasattr(item, 'id'):
            item.__class__.last_id += 1
            item.id = item.__class__.last_id
        if hasattr(item, 'project'):
            item.project_id = item.project.id
        if hasattr(item, 'category'):
            item.category_id = item.category.id
        key = item.__class__.__name__ + '.' + str(item.id)
        self.data[key] = item

    def delete_item(self, item):
        key = item.__class__.__name__ + '.' + str(item.id)
        del self.data[key]

    def update_item(self, item):
        key = item.__class__.__name__ + '.' + str(item.id)
        del self.data[key]
        self.data[key] = item

    def get_first_item(self, cls):
        for key, obj in self.data.iteritems():
            if key.startswith(cls.__name__):
                return obj

    def get_items(self, cls, flt = None):
        items = []
        for key, obj in self.data.iteritems():
            if key.startswith(cls.__name__):
                found = True
                if flt is not None:
                    for attr, val in flt.iteritems():
                        if not hasattr(obj, attr) or getattr(obj, attr) != val:
                            found = False
                            break
                if found:
                    items.append(obj)
        return sorted(items, cmp=lambda x,y: cmp(x.name, y.name))

    def get_item(self, cls, flt = None):
        items = self.get_items(cls, flt)
        if len(items) == 0:
            return None
        else:
            return items[0]

    def bulk_update(self, cls, changes, flt = None):
        print('bulk_update')
