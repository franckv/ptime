import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, Project, Category, Task
import config

class DB(object):
    def __init__(self):
        engine = create_engine(config.engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    def close(self):
        if self.session:
            try:
                self.session.commit()
            except:
                self.session.close()

    def create(self):
        Base.metadata.create_all(self.session.bind)

    def drop(self):
        Base.metadata.drop_all(self.session.bind)

    def reset(self):
        for table in (Project, Category, Task):
            if table.__table__.exists(self.session.bind):
                self.session.connection().execute(table.__table__.delete())
        self.session.commit()

    def get_tasks(self, project, category):
        results = []

        query = self.session.query(Task).join(Category.tasks).join(Category.project).filter(Category.name == category).filter(Project.name == project)
        for task in query.all():
            results.append(task)

        return results

    def create_project(self, name):
        query = self.session.query(Project)
        if len(query.all()) > 0:
            print('Project already exists')
            return

        proj = Project(name)
        self.session.add(proj)

        self.session.commit()

    def create_category(self, project, name):
        project = self.get_project(project)
        query = self.session.query(Category).filter(Category.name == name).filter(Category.project_id == project.id)
        if len(query.all()) > 0:
            print('Category already exists')
            return

        category = Category(name)
        category.project = project
        self.session.add(category)

        self.session.commit()

    def create_task(self, project, category, name):
        project = self.get_project(project)
        category = self.get_category(project, category)
        if category is None:
            print('Invalid category')
            return

        query = self.session.query(Task).filter(Task.name == name).filter(Task.category_id == category.id)
        if len(query.all()) > 0:
            print('Task already exists')
            return

        task = Task(name)
        task.category_id = category.id
        self.session.add(task)

        self.session.commit()

    def get_project(self, name):
        if isinstance(name, Project):
            return name
        query = self.session.query(Project).filter(Project.name == name)
        projects = query.all()
        if len(projects) == 1:
            return projects[0]
        else:
            return None

    def get_categories(self, project):
        if not isinstance(project, Project):
            project = self.get_project(project)

        if project is None:
            print('Invalid project')
            return None

        query = self.session.query(Category).filter(Category.project_id == project.id)
        categories = query.all()

        return categories

    def get_category(self, project, name):
        if isinstance(name, Category):
            return name
        if not isinstance(project, Project):
            project = self.get_project(project)

        if project is None:
            print('Invalid project')
            return None

        query = self.session.query(Category).filter(Category.name == name).filter(Category.project_id == project.id)
        categories = query.all()

        if len(categories) == 1:
            return categories[0]
        else:
            return None

    def get_task(self, project, category, name):
        if isinstance(name, Task):
            return name
        if not isinstance(project, Project):
            project = self.get_project(project)
        if not isinstance(category, Category):
            category = self.get_category(project, category)

        if category is None:
            print('Invalid category')
            return None

        query = self.session.query(Task).filter(Task.name == name).filter(Task.category_id == category.id)
        tasks = query.all()

        if len(tasks) == 1:
            return tasks[0]
        else:
            return None

    def disable_task(self, project, category, name):
        task = self.get_task(project, category, name)

        task.enabled = False 

        self.session.commit()

    def enable_task(self, project, category, name):
        task = self.get_task(project, category, name)

        task.enabled = True 

        self.session.commit()
