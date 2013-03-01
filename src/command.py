import os, os.path
import inspect

import config
from model import Project, Category, Task
from backend import get_backend
from utils import Utils

class Command(object):
    def __init__(self):
        backend = get_backend(config)
        self.utils = Utils(backend)
        self.list = {}

        for func in dir(self):
            if func.startswith('do_'):
                f = getattr(Command, func)
                self.list[func[3:]] = {'args': len(inspect.getargspec(f).args) - 1, 'exec': f}

    def do_list(self, project, category):
        tasks = self.utils.get_project_tasks(project, category)
        if tasks is None:
            print('No tasks')
        else:
            for task in tasks:
                disabled = '' if task.enabled else '(Disabled)'
                print('%s %s' % (task.name, disabled))

    def do_create_project(self, name):
        project = self.utils.create_project(name)
    
    def do_get_default_project(self):
        project = self.utils.get_default_project()
        print(project)

    def do_get_project(self, name):
        project = self.utils.get_project(name)
        print(project)

    def do_set_project(self, name):
        project = self.utils.set_project(name)

    def do_get_projects(self):
        projects = self.utils.get_projects()
        print(projects)

    def do_create_category(self, category):
        category = self.utils.create_category(category)

    def do_create_project_category(self, project, category):
        category = self.utils.create_project_category(project, category)

    def do_get_category(self, project, name):
        category = self.utils.get_category(project, name)
        print(category)

    def do_get_categories(self):
        categories = self.utils.get_categories()
        print(categories)

    def do_get_project_categories(self, project):
        categories = self.utils.get_project_categories(project)
        print(categories)

    def do_create_task(self, category, name):
        task = self.utils.create_task(category, name)

    def do_create_project_task(self, project, category, name):
        task = self.utils.create_project_task(project, category, name)
        
    def do_enable_task(self, project, category, name):
        self.utils.enable_task(project, category, name)

    def do_disable_task(self, project, category, name):
        self.utils.disable_task(project, category, name)

    def do_delete_task(self, project, category, name):
        self.utils.delete_task(project, category, name)

    def do_get_tasks(self, category):
        tasks = self.utils.get_tasks(category)
        if tasks is not None:
            print(tasks)

    def do_check_db(self):
        self.utils.check_db()

    def do_reset(self):
        self.utils.reset()

    def do_create(self):
        self.utils.create()

    def do_drop(self):
        self.utils.drop()

    def close(self):
        self.utils.close()

