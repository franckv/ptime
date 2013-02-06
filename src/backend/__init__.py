from model import Project, Category, Task

def get_backend(config):
    from .db import DB
    return DB()

class Backend(object):
    def __init__(self):
        pass

    # projects

    def project_exists(self, project):
        return False

    def create_project(self, project):
        if self.item_exists(Project, {Project.name: project}):
            print('Project already exists')
            return

        proj = Project(project)
        self.add_item(proj)

        return project

    def set_project(self, project):
        if not isinstance(project, Project):
            project = self.get_project(project)

        if project is None:
            return

        self.set_project_default(project)

    def get_projects(self):
        return self.get_items(Project)

    def get_project(self, project):
        if isinstance(project, Project):
            return project

        return self.get_item(Project, {Project.name: project})

    def get_default_project(self):
        project = self.get_item(Project, {Project.default: True})
        if project is None:
            return self.get_first_item(Project)

        return project

    def set_project_default(self, project):
        if not isinstance(project, Project):
            project = self.get_project(project)

        if project is None:
            return

        self.bulk_update(Project, {Project.default: False})
        project.default = True

        self.update_item(project)

    # categories

    def create_category(self, category):
        project = self.get_default_project()

        return self.create_project_category(project, category)

    def create_project_category(self, project, category):
        project = self.get_project(project)
        if self.item_exists(Category, {Category.name: category, Category.project_id: project.id}):
            print('Category already exists')
            return

        cat = Category(category)
        cat.project = project

        self.add_item(cat)

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
        self.delete_item(category)

    def get_category(self, project, category):
        if isinstance(category, Category):
            return category
        if not isinstance(project, Project):
            project = self.get_project(project)

        if project is None:
            print('Invalid project')
            return None

        return self.get_item(Category, {Category.name: category, Category.project_id: project.id})

    def get_project_categories(self, project):
        if not isinstance(project, Project):
            project = self.get_project(project)

        if project is None:
            print('Invalid project')
            return None

        categories = self.get_items(Category, {Category.project_id: project.id})

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

        if self.item_exists(Task, {Task.name: name, Task.category_id: cat.id}):
            print('Task already exists')
            return

        task = Task(name)
        task.category_id = cat.id

        self.add_item(task)

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

        return self.get_items(Task, {Task.category_id: category.id})

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

        return self.get_item(Task, {Task.name: task, Task.category_id: category.id})

    def delete_project_task(self, project, category, name):
        task = self.get_task(project, category, name)
        self.delete_item(task)

    def disable_task(self, project, category, name):
        task = self.get_task(project, category, name)

        task.enabled = False 

        self.update_item(task)

    def enable_task(self, project, category, name):
        task = self.get_task(project, category, name)

        task.enabled = True 

        self.update_item(task)
