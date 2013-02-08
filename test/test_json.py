#!/usr/bin/env python2

import sys
import json
import unittest

sys.path.insert(0, '../src')

from model import Project, Category, Task
import config_test as config
from backend.jsonbackend import ModelEncoder, JSon
from backend.db import DB

class TestJSon(unittest.TestCase):
    def test_encoder(self):
        p = Project('test')
        p.id = 1
        c = Category('test')
        c.id = 2
        c.project_id = p.id
        t = Task('test')
        t.id = 3
        t.category_id = c.id

        self.assertIsNotNone(json.dumps(p, cls=ModelEncoder))
        self.assertIsNotNone(json.dumps(c, cls=ModelEncoder))
        self.assertIsNotNone(json.dumps(t, cls=ModelEncoder))

    def test_generate_json(self):
        db = DB(config.backend_db['engine'])

        projects = db.get_items(Project)
        categories = db.get_items(Category)
        tasks = db.get_items(Task)

        s = json.dumps(projects+categories+tasks, cls=ModelEncoder, separators=(',', ':'))
        self.assertIsNotNone(s)

        f = open(config.backend_json['filename'], 'w')
        f.write(s)
        f.close()

    def test_load_json(self):
        j = JSon(config.backend_json['filename'])
        
    def test_add_item(self):
        j = JSon(config.backend_json['filename'])

        t = Task('new task')
        t.id = 3
        t.category_id=1

        key = 'Task.3'

        j.add_item(t)
        j.commit()

        self.assertIn(key, j.data.keys())

    def test_update_item(self):
        j = JSon(config.backend_json['filename'])

        t = Task('new task')
        t.id = 3
        t.category_id=1

        key = 'Task.3'

        j.update_item(t)
        j.commit()

        self.assertIn(key, j.data.keys())

    def test_delete_item(self):
        j = JSon(config.backend_json['filename'])

        t = Task('new task')
        t.id = 3
        t.category_id=1

        key = 'Task.3'

        j.delete_item(t)
        j.commit()

        self.assertNotIn(key, j.data.keys())

    def test_get_item(self):
        j = JSon(config.backend_json['filename'])

        p = j.get_item(Project, {Project.default: True})
        self.assertIsInstance(p, Project)
        self.assertTrue(p.default)
        p = j.get_item(Project, {Project.default: False})
        self.assertIsInstance(p, Project)
        self.assertFalse(p.default)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestJSon('test_encoder'))
    suite.addTest(TestJSon('test_generate_json'))
    suite.addTest(TestJSon('test_load_json'))
    suite.addTest(TestJSon('test_add_item'))
    suite.addTest(TestJSon('test_update_item'))
    suite.addTest(TestJSon('test_delete_item'))
    suite.addTest(TestJSon('test_get_item'))
    result = unittest.TestResult()
    suite.run(result)
    print('Errors: ' + str(result.errors))

