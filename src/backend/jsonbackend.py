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
