import kivy
from kivy.app import App
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

        if node is None:
            return

        item = node.item

        if isinstance(item, Category):
            name = 'new task3'
            self.app.backend.create_project_task(item.project, item, name)

            self.app.on_select_node(self.projects, node)

    def btn_delete(self):
        if len(self.scroll.children) > 0:
            for child in self.scroll.children[0].children:
                label, check = child.children
                if check.active:
                    item = label.item
                    self.app.backend.delete_project_task(item.category.project, item.category, item)
            node = self.projects.selected_node
            self.app.on_select_node(self.projects, node)

Factory.register('PTimeWidget', cls=PTimeWidget)

class PTimeApp(App):
    def build(self):
        self.window = PTimeWidget()
        self.window.app = self
        self.backend = get_backend(config) 

        self.build_tree(self.window.projects)

        self.window.projects.bind(selected_node=self.on_select_node)

        return self.window

    def build_tree(self, tree):
        while not tree.root.is_leaf:
            tree.remove_node(tree.root.nodes[0])

        projects = self.backend.get_projects()
        for project in projects:
            print(project.default)
            p = tree.add_node(TreeViewLabel(text=project.name, is_open=project.default, no_selection=True))
            categories = self.backend.get_project_categories(project)
            for category in categories:
                c = tree.add_node(TreeViewLabel(text=category.name, is_open=True, no_selection=False), p)
                c.item = category
                tasks = self.backend.get_project_tasks(project, category)

    def on_select_node(self, tree, node):
        grid = GridLayout(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        if len(self.window.scroll.children) > 0: self.window.scroll.remove_widget(self.window.scroll.children[0])
        self.window.scroll.add_widget(grid)

        item = node.item

        if isinstance(item, Category):
            tasks = self.backend.get_project_tasks(item.project, item)

            for task in tasks:
                layout = BoxLayout(size_hint_y=None)
                check = CheckBox(size_hint_x=None)
                lbl = Label(text=task.name)
                lbl.item = task
                layout.add_widget(check)
                layout.add_widget(lbl)
                grid.add_widget(layout)

