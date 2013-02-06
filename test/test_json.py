#!/usr/bin/env python2

import sys
import json

sys.path.append('../src')

from model import Project, Category, Task
from backend.jsonbackend import ModelEncoder

p = Project('test')
p.id = 1
c = Category('test')
c.id = 2
c.project_id = p.id
t = Task('test')
t.id = 3
t.category_id = c.id
print(json.dumps(p, cls=ModelEncoder))
print(json.dumps(c, cls=ModelEncoder))
print(json.dumps(t, cls=ModelEncoder))
