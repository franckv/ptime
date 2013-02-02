from sqlalchemy import Table, Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relation, backref, validates
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    default = Column(Boolean)

    def __init__(self, name):
        self.name = name
        self.default = False

    def __repr__(self):
        return "<Project('%s')>" % self.name

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    project_id = Column(Integer, ForeignKey(Project.id))

    project = relation(Project, backref=backref('categories'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Category('%s')>" % self.name

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id))
    enabled = Column(Boolean)

    category = relation(Category, backref=backref('tasks'))

    def __init__(self, name):
        self.name = name
        self.enabled = True

    def __repr__(self):
        return "<Task('%s')>" % self.name

