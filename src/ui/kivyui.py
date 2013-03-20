import sys

import kivy
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

import config
from widgets import TitleBox, PopupBox, InputBox, ConfirmBox, SelectBox
from utils import Utils
from backend import get_backend
from model import Category

class MainScreen(Screen):
    project = StringProperty('<none>')
    def btn_add_project(self):
        inputbox = InputBox(title='New project', on_done=self.add_project)
        inputbox.open()

    def add_project(self, value):
        if value is not None and len(value) > 0:
            project = self.manager.app.utils.create_project(value)
            self.manager.app.utils.set_project_default(project)
            self.manager.app.set_project(project)
            self.open_project()

    def btn_select_project(self):
        project = self.manager.app.project
        values = []
        for proj in self.manager.app.utils.get_projects():
            values.append(proj.name)

        selectbox = SelectBox(title='Select project', values=values, default=project.name, on_done=self.select_project)
        selectbox.open()

    def select_project(self, value):
        if value is not None and len(value) > 0:
            project = self.manager.app.utils.get_project(value)
            self.manager.app.set_project(project)
            self.open_project()

    def open_project(self):
        self.manager.transition.direction='left'
        self.manager.current = 'project'

class ProjectScreen(Screen):
    project = StringProperty('<none>')
    def btn_add_category(self):
        project = self.manager.app.project
        inputbox = InputBox(title='New category', on_done=self.add_category, ctx=[project])
        inputbox.open()

    def add_category(self, value, project):
        if value is not None and len(value) > 0:
            self.manager.app.utils.create_project_category(project, value)
            self.manager.app.update_categories(project)

    def back(self):
        self.manager.transition.direction='right'
        self.manager.current='main'

    def btn_delete_project(self):
        project = self.manager.app.project
        confirmbox = ConfirmBox(title='Delete project?', on_done=self.delete_project, ctx=[project])
        confirmbox.open()

    def delete_project(self, project):
        self.manager.app.utils.delete_project(project)
        project = self.manager.app.utils.get_default_project()
        self.manager.app.set_project(project)
        self.back()

    def btn_schedule(self):
        project = self.manager.app.project
        schedule = self.manager.app.utils.schedule_tasks(project)
        for task in schedule:
            print(task.name + '(' + str(self.manager.app.utils.get_task_priority(task)) + ')' + ' cat ' + str(task.category_id))

class CategoryScreen(Screen):
    project = StringProperty('<none>')
    category = StringProperty('<none>')
    def btn_add_task(self):
        project = self.manager.app.project
        category = self.manager.app.category
        inputbox = InputBox(title='New Task', on_done=self.add_task, ctx=[project, category])
        inputbox.open()

    def add_task(self, value, project, category):
        if value is not None and len(value) > 0:
            self.manager.app.utils.create_project_task(project, category, value)
            self.manager.app.update_tasks(project, category)

    def back(self):
        self.manager.transition.direction='right'
        self.manager.current='project'

    def btn_delete_category(self):
        project = self.manager.app.project
        category = self.manager.app.category
        confirmbox = ConfirmBox(title='Delete category and all tasks?', on_done=self.delete_category, ctx=[project, category])
        confirmbox.open()

    def delete_category(self, project, category):
        self.manager.app.utils.delete_project_category(project, category)
        self.manager.app.update_categories(project)
        self.back()

class TaskScreen(Screen):
    project = StringProperty('<none>')
    category = StringProperty('<none>')
    task = StringProperty('<none>')
    def back(self):
        self.manager.transition.direction='right'
        self.manager.current='category'

    def btn_delete_task(self):
        project = self.manager.app.project
        category = self.manager.app.category
        task = self.manager.app.task
        confirmbox = ConfirmBox(title='Delete task?', on_done=self.delete_task, ctx=[project, category, task])
        confirmbox.open()

    def delete_task(self, project, category, task):
        self.manager.app.utils.delete_project_task(project, category, task)
        self.manager.app.update_tasks(project, category)
        self.back()

class PTimeApp(App):
    def build(self):
        self.screens = ScreenManager(transition=SlideTransition())
        self.screens.app = self
        self.screens.add_widget(MainScreen(name='main'))
        self.screens.add_widget(ProjectScreen(name='project'))
        self.screens.add_widget(CategoryScreen(name='category'))
        self.screens.add_widget(TaskScreen(name='task'))
        self.screens.current = 'main'

        backend = get_backend(config) 
        self.utils = Utils(backend)
        project = self.utils.get_default_project()
        self.set_project(project)

        categories = self.screens.get_screen('project')
        categories.grid.bind(minimum_height=categories.grid.setter('height'))

        return self.screens

    def set_project(self, project):
        if project is None:
            return
        self.project = project
        self.screens.get_screen('main').project = self.project.name
        self.screens.get_screen('project').project = self.project.name
        self.screens.get_screen('category').project = self.project.name
        self.screens.get_screen('task').project = self.project.name
        self.update_categories(project)

    def update_categories(self, project):
        grid = self.screens.get_screen('project').grid
        grid.clear_widgets()
        for category in self.utils.get_project_categories(project):
            lbl = Button(text=category.name, size_hint_y=None)
            lbl.height = dp(44)
            lbl.bind(on_release=lambda btn, category=category: self.select_category(category))

            grid.add_widget(lbl)

    def select_category(self, category):
        self.category = category
        self.screens.get_screen('category').category = self.category.name
        self.screens.get_screen('task').category = self.category.name
        self.update_tasks(self.project, category)
        self.screens.transition.direction='left'
        self.screens.current='category'

    def update_tasks(self, project, category):
        grid = self.screens.get_screen('category').grid
        grid.clear_widgets()
        for task in self.utils.get_project_tasks(project, category):
            lbl = Button(text=task.name, size_hint_y=None)
            lbl.height = dp(44)
            lbl.bind(on_release=lambda btn, task=task: self.select_task(task))

            grid.add_widget(lbl)

    def select_task(self, task):
        self.task = task
        self.screens.get_screen('task').task = self.task.name
        self.screens.transition.direction='left'
        self.screens.current='task'
