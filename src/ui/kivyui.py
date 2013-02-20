import sys

import kivy
from kivy.app import App
from kivy.metrics import dp
from kivy.factory import Factory
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
        inputbox = InputBox(title='New project')
        inputbox.done.bind(on_release=lambda btn, inputbox=inputbox, value=inputbox.value: self.add_project(inputbox, value))
        inputbox.open()

    def add_project(self, inputbox, value):
        inputbox.close()
        if value.text is not None and len(value.text) > 0:
            project = self.manager.app.utils.create_project(value.text)
            self.manager.app.utils.set_project_default(project)
            self.manager.app.set_project(project)

    def btn_select_project(self):
        selectbox = SelectBox(title='Select project')

        project = self.manager.app.project

        for proj in self.manager.app.utils.get_projects():
            selectbox.values.values.append(proj.name)

        selectbox.values.text = project.name

        selectbox.done.bind(on_release=lambda btn, selectbox=selectbox, values=selectbox.values: self.select_project(selectbox, values))
        selectbox.open()

    def select_project(self, selectbox, values):
        selectbox.close()
        if values.text is not None and len(values.text) > 0:
            project = self.manager.app.utils.get_project(values.text)
            self.manager.app.set_project(project)
            self.open_project()

    def open_project(self):
        self.manager.transition.direction='left'
        self.manager.current = 'project'

class ProjectScreen(Screen):
    def btn_add_category(self):
        project = self.manager.app.project
        inputbox = InputBox(title='New category')
        inputbox.done.bind(on_release=lambda btn, inputbox=inputbox, value=inputbox.value, project=project: self.add_category(inputbox, value, project))
        inputbox.open()

    def add_category(self, inputbox, value, project):
        inputbox.close()
        if value.text is not None and len(value.text) > 0:
            self.manager.app.utils.create_project_category(project, value.text)
            self.manager.app.update_categories(project)

    def back(self):
        self.manager.transition.direction='right'
        self.manager.current='main'

class CategoryScreen(Screen):
    def btn_add_task(self):
        project = self.manager.app.project
        category = self.manager.app.category
        inputbox = InputBox(title='New Task')
        inputbox.done.bind(on_release=lambda btn, inputbox=inputbox, value=inputbox.value, project=project, category=category: self.add_task(inputbox, value, project, category))
        inputbox.open()

    def add_task(self, inputbox, value, project, category):
        inputbox.close()
        if value.text is not None and len(value.text) > 0:
            self.manager.app.utils.create_project_task(project, category, value.text)
            self.manager.app.update_tasks(project, category)

    def back(self):
        self.manager.transition.direction='right'
        self.manager.current='project'

    def btn_delete_category(self):
        project = self.manager.app.project
        category = self.manager.app.category
        confirmbox = ConfirmBox(title='Delete category and all tasks?')
        confirmbox.done.bind(on_release=lambda btn, confirmbox=confirmbox, project=project, category=category: self.delete_category(confirmbox, project, category))
        confirmbox.open()

    def delete_category(self, confirmbox, project, category):
        confirmbox.close()
        self.manager.app.utils.delete_project_category(project, category)

Factory.register('MainScreen', cls=MainScreen)
Factory.register('ProjectScreen', cls=ProjectScreen)
Factory.register('CategoryScreen', cls=CategoryScreen)

class PTimeApp(App):
    def build(self):
        self.screens = ScreenManager(transition=SlideTransition())
        self.screens.app = self
        self.screens.add_widget(MainScreen(name='main'))
        self.screens.add_widget(ProjectScreen(name='project'))
        self.screens.add_widget(CategoryScreen(name='category'))
        self.screens.current = 'main'

        backend = get_backend(config) 
        self.utils = Utils(backend)
        project = self.utils.get_default_project()
        self.set_project(project)

        categories = self.screens.get_screen('project')
        categories.grid.bind(minimum_height=categories.grid.setter('height'))

        return self.screens

    def set_project(self, project):
        self.project = project
        self.screens.get_screen('main').project = self.project.name
        self.update_categories(project)

    def update_categories(self, project):
        grid = self.screens.get_screen('project').grid
        grid.clear_widgets()
        for cat in self.utils.get_project_categories(project):
            lbl = Button(text=cat.name, size_hint_y=None)
            lbl.height = dp(44)
            lbl.bind(on_release=lambda btn, category=cat.name: self.select_category(category))

            grid.add_widget(lbl)

    def select_category(self, category):
        self.category = category
        self.update_tasks(self.project, category)
        self.screens.transition.direction='left'
        self.screens.current='category'

    def update_tasks(self, project, category):
        grid = self.screens.get_screen('category').grid
        grid.clear_widgets()
        for task in self.utils.get_project_tasks(project, category):
            lbl = Button(text=task.name, size_hint_y=None)
            lbl.height = dp(44)
            lbl.bind(on_release=lambda btn, project=project, category=category, task=task.name: self.select_task(project, category, task))

            grid.add_widget(lbl)

    def select_task(self, project, category, task):
        pass
