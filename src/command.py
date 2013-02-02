import os, os.path
import inspect

import config
from model import Project, Category, Task
from backend import get_backend

class Command(object):
    def __init__(self):
        self.backend = get_backend(config)
        self.list = {}

        for func in dir(self):
            if func.startswith('do_'):
                f = getattr(Command, func)
                self.list[func[3:]] = {'args': len(inspect.getargspec(f).args) - 1, 'exec': f}

    def do_list(self, project, category):
        tasks = self.backend.get_tasks(project, category)
        for task in tasks:
            disabled = '' if task.enabled else '(Disabled)'
            print('%s %s' % (task.name, disabled))

    def do_create_project(self, name):
        project = self.backend.create_project(name)
    
    def do_get_default_project(self):
        project = self.backend.get_default_project()
        print(project)

    def do_get_project(self, name):
        project = self.backend.get_project(name)
        print(project)

    def do_set_project(self, name):
        project = self.backend.set_project(name)

    def do_get_projects(self):
        projects = self.backend.get_projects()
        print(projects)

    def do_create_category(self, category):
        category = self.backend.create_category(category)

    def do_create_project_category(self, project, category):
        category = self.backend.create_category(project, category)

    def do_get_category(self, project, name):
        category = self.backend.get_category(project, name)
        print(category)

    def do_get_categories(self):
        categories = self.backend.get_categories()
        print(categories)

    def do_get_project_categories(self, project):
        categories = self.backend.get_project_categories(project)
        print(categories)

    def do_create_task(self, category, name):
        task = self.backend.create_task(category, name)

    def do_create_project_task(self, project, category, name):
        task = self.backend.create_project_task(project, category, name)
        
    def do_enable_task(self, project, category, name):
        self.backend.enable_task(project, category, name)

    def do_disable_task(self, project, category, name):
        self.backend.disable_task(project, category, name)

    def do_get_tasks(self, category):
        tasks = self.backend.get_tasks(category)
        if tasks is not None:
            print(tasks)

    def do_check_db(self):
        self.backend.check_db()

    def do_reset(self):
        self.backend.reset()

    def do_create(self):
        self.backend.create()

    def do_drop(self):
        self.backend.drop()

    def close(self):
        self.backend.close()

