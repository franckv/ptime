class Project(object):
    def __init__(self, name):
        self.name = name
        self.default = False

    def __repr__(self):
        return "<Project('%s')>" % self.name

class Category(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Category('%s')>" % self.name

class Task(object):
    def __init__(self, name):
        self.name = name
        self.enabled = True
        self.duration = 5
        self.rating = 0
        self.completed = 0

    def __repr__(self):
        return "<Task('%s')>" % self.name

