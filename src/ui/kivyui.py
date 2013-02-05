import kivy
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox

import config
from backend import get_backend
from model import Category

class PTimeWidget(FloatLayout):
    def btn_add(self):
        node = self.projects.selected_node

        if not hasattr(node, 'item'):
            return

        if not node.is_selected:
            return

        item = node.item

        if isinstance(item, Category):
            name = 'new task3'
            self.app.backend.create_project_task(item.project, item, name)

            self.app.on_select_node(self.projects, node)

    def btn_delete(self):
        if len(self.grid.children) > 0:
            for child in self.grid.children:
                label, check = child.children
                if check.active:
                    item = label.item
                    self.app.backend.delete_project_task(item.category.project, item.category, item)
            node = self.projects.selected_node
            if node is not None and node.is_selected:
                self.app.on_select_node(self.projects, node)

Factory.register('PTimeWidget', cls=PTimeWidget)

class PTimeApp(App):
    def build(self):
        self.window = PTimeWidget()
        self.window.app = self
        self.backend = get_backend(config) 
        default_project = self.backend.get_default_project()
        self.window.drop_project.text = default_project.name
        for proj in self.backend.get_projects():
            self.window.drop_project.values.append(proj.name)

        self.window.drop_project.bind(text=self.select_project)

        self.build_tree(default_project, self.window.projects)

        self.window.projects.bind(selected_node=self.on_select_node)

        self.window.grid.bind(minimum_height=self.window.grid.setter('height'))

        return self.window

    def select_project(self, menu, value):
        project = self.backend.get_project(value)
        self.build_tree(project, self.window.projects)

        if self.window.projects.selected_node is not None:
            self.window.projects.selected_node.is_selected = False
            self.on_select_node(None, None)

    def build_tree(self, project, tree):
        while not tree.root.is_leaf:
            tree.remove_node(tree.root.nodes[0])

        #p = tree.add_node(TreeViewLabel(text=project.name, is_open=project.default, no_selection=True))
        categories = self.backend.get_project_categories(project)
        for category in categories:
            c = tree.add_node(TreeViewLabel(text=category.name, is_open=True, no_selection=False))
            c.item = category
            tasks = self.backend.get_project_tasks(project, category)

    def on_select_node(self, tree, node):
        self.window.grid.clear_widgets()

        if not hasattr(node, 'item'):
            return

        item = node.item

        if isinstance(item, Category):
            tasks = self.backend.get_project_tasks(item.project, item)

            for task in tasks:
                layout = BoxLayout(size_hint_y=None)
                layout.height = dp(24)
                check = CheckBox(size_hint_x=None)
                lbl = Label(text=task.name, halign='left')
                lbl.item = task
                lbl.text_size = (lbl.width, None)
                layout.add_widget(check)
                layout.add_widget(lbl)
                self.window.grid.add_widget(layout)

