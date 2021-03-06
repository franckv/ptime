from math import log
from model import Project, Category, Task

class Utils(object):
    def __init__(self, backend):
        self.backend = backend

    # projects

    def project_exists(self, project):
        return False

    def create_project(self, project):
        if self.backend.item_exists(Project, {'name': project}):
            print('Project already exists')
            return

        proj = Project(project)
        self.backend.add_item(proj)
        self.backend.commit()

        return proj

    def set_project(self, project):
        if not isinstance(project, Project):
            project = self.get_project(project)

        if project is None:
            return

        self.set_project_default(project)
        self.backend.commit()

    def get_projects(self):
        return self.backend.get_items(Project)

    def get_project(self, project):
        if isinstance(project, Project):
            return project

        return self.backend.get_item(Project, {'name': project})

    def get_default_project(self):
        project = self.backend.get_item(Project, {'default': True})
        if project is None:
            return self.backend.get_first_item(Project)

        return project

    def set_project_default(self, project):
        if not isinstance(project, Project):
            project = self.get_project(project)

        if project is None:
            return

        self.backend.bulk_update(Project, {'default': False})
        project.default = True

        self.backend.update_item(project)
        self.backend.commit()

    def delete_project(self, project):
        if not isinstance(project, Project):
            project = self.get_project(project)

        if project is None:
            return

        categories = self.get_project_categories(project)
        for category in categories:
            self.delete_project_category(project, category)
        self.backend.delete_item(project)
        self.backend.commit()

    def schedule_tasks(self, project, duration=60):
        schedule = []

        all_tasks = self.get_all_tasks(project)
        if all_tasks is None:
            return None

        # sort tasks by priority
        all_tasks = sorted(all_tasks, cmp=lambda x,y: cmp(self.get_task_priority(x), self.get_task_priority(y)), reverse=True)

        # split sorted tasks in categories
        categories = {}
        for task in all_tasks:
            if task.category_id not in categories:
                categories[task.category_id] = []
            categories[task.category_id].append(task)

        # interleave categories if more than one
        if len(categories) > 1:
            all_tasks = [y for x in map(None, *categories.values()) for y in x]

        d = 0
        for task in [t for t in all_tasks if not t is None]:
            if d + task.duration <= duration:
                schedule.append(task)
                d += task.duration

        return schedule

    # categories

    def create_category(self, category):
        project = self.get_default_project()

        return self.create_project_category(project, category)

    def create_project_category(self, project, category):
        project = self.get_project(project)

        if project is None:
            print('Invalid project')
            return

        if self.backend.item_exists(Category, {'name': category, 'project_id': project.id}):
            print('Category already exists')
            return

        cat = Category(category)
        cat.project = project

        self.backend.add_item(cat)
        self.backend.commit()

        return cat

    def delete_category(self, category):
        project = self.get_default_project()

        return self.delete_project_category(project, category)

    def delete_project_category(self, project, category):
        project = self.get_project(project)

        if not isinstance(category, Category):
            category = self.get_category(project, category)

        tasks = self.get_project_tasks(project, category)
        for task in tasks:
            self.delete_project_task(project, category, task)
        self.backend.delete_item(category)
        self.backend.commit()

    def get_category(self, project, category):
        if isinstance(category, Category):
            return category
        if not isinstance(project, Project):
            project = self.get_project(project)

        if project is None:
            print('Invalid project')
            return None

        return self.backend.get_item(Category, {'name': category, 'project_id': project.id})

    def get_project_categories(self, project):
        if not isinstance(project, Project):
            project = self.get_project(project)

        if project is None:
            print('Invalid project')
            return None

        categories = self.backend.get_items(Category, {'project_id': project.id})

        return categories

    def get_categories(self):
        project = self.get_default_project()

        if project is None:
            print('Invalid project')
            return None

        return self.get_project_categories(project)

    # tasks

    def create_task(self, category, name):
        project = self.get_default_project()
        return self.create_project_task(project, category, name)

    def create_project_task(self, project, category, name):
        if project is None:
            print('Invalid project')
            return None

        cat = self.get_category(project, category)
        if cat is None:
            cat = self.create_project_category(project, category)

        if self.backend.item_exists(Task, {'name': name, 'category_id': cat.id}):
            print('Task already exists')
            return

        task = Task(name)
        task.category_id = cat.id

        self.backend.add_item(task)
        self.backend.commit()

        return task

    def get_tasks(self, category):
        project = self.get_default_project()
        if project is None:
            print('No project')
            return None

        return self.get_project_tasks(project, category)

    def get_project_tasks(self, project, category):
        if not isinstance(project, Project):
            project = self.get_project(project)

        if project is None:
            print('Invalid project')
            return None

        if not isinstance(category, Category):
            category = self.get_category(project, category)

        if category is None:
            print('Invalid category')
            return None

        return self.backend.get_items(Task, {'category_id': category.id})

    def get_all_tasks(self, project):
        all_tasks = []

        if project is None:
            print('Invalid project')
            return None

        categories = self.get_project_categories(project)
        for category in categories:
            tasks = self.get_project_tasks(project, category)
            for task in tasks:
                all_tasks.append(task)

        return all_tasks

    def get_task(self, project, category, task):
        if isinstance(task, Task):
            return task
        if not isinstance(project, Project):
            project = self.get_project(project)
        if not isinstance(category, Category):
            category = self.get_category(project, category)

        if category is None:
            print('Invalid category')
            return None

        return self.backend.get_item(Task, {'name': task, 'category_id': category.id})

    def delete_project_task(self, project, category, name):
        task = self.get_task(project, category, name)
        self.backend.delete_item(task)
        self.backend.commit()

    def disable_task(self, project, category, name):
        task = self.get_task(project, category, name)

        task.enabled = False 

        self.backend.update_item(task)
        self.backend.commit()

    def enable_task(self, project, category, name):
        task = self.get_task(project, category, name)

        task.enabled = True 

        self.backend.update_item(task)
        self.backend.commit()

    def get_task_priority(self, task):
        return int(10*(5-task.rating)/(1+log(1+task.completed)))

    # backend

    def create(self):
        self.backend.create()

    def drop(self):
        self.backend.drop()

    def close(self):
        self.backend.close()
