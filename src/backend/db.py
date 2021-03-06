import logging

from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData, Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, backref, mapper, relationship
from sqlalchemy.exc import OperationalError
import sqlalchemy

from model import Project, Category, Task
from . import Backend
import config

class DB(Backend):
    def __init__(self, engine):
        engine = create_engine(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.metadata = MetaData()

        project = Table('project', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String),
                Column('default', Boolean))

        category = Table('category', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String),
                Column('project_id', Integer, ForeignKey('project.id')))

        task = Table('task', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String, nullable=False),
                Column('enabled', Boolean),
                Column('category_id', Integer, ForeignKey('category.id')))

        mapper(Task, task)

        mapper(Category, category, properties = {
                'tasks' : relationship(Task, backref='category')
        })

        mapper(Project, project, properties = {
                'categories' : relationship(Category, backref='project')
        })

        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    def close(self):
        if self.session:
            try:
                self.commit()
            except:
                self.session.close()

    def commit(self):
        self.session.commit()

    def create(self):
        try:
            self.metadata.create_all(self.session.bind)
        except OperationalError:
            print('Cannot create DB %s' % config.engine)

    def drop(self):
        try:
            self.metadata.drop_all(self.session.bind)
        except OperationalError:
            print('Cannot drop DB %s' % config.engine)

    def reset(self):
        for table in (Project, Category, Task):
            if table.__table__.exists(self.session.bind):
                self.session.connection().execute(table.__table__.delete())
        self.commit()

    def apply_filter(self, cls, query, flt):
        if flt is not None:
            for col, val in flt.items():
                query = query.filter(getattr(cls, col) == val)

        return query

    def item_exists(self, cls, flt = None):
        query = self.session.query(cls)
        query = self.apply_filter(cls, query, flt)

        return len(query.all()) > 0

    def add_item(self, item):
        self.session.add(item)
        self.commit()

    def delete_item(self, item):
        self.session.delete(item)
        self.commit()

    def update_item(self, item):
        if item not in self.session:
            self.session.add(item)

        self.commit()

    def get_first_item(self, cls):
        query = self.session.query(cls)
        results = query.all()
        if len(results) > 0:
            return results[0]
        else:
            return None

    def get_items(self, cls, flt = None):
        query = self.session.query(cls)
        query = self.apply_filter(cls, query, flt)
        return query.all()

    def get_item(self, cls, flt = None):
        results = self.get_items(cls, flt)
        if len(results) == 1:
            return results[0]
        else:
            return None

    def bulk_update(self, cls, changes, flt = None):
        query = self.session.query(cls)
        query = self.apply_filter(cls, query, flt)
        query.update(changes)
        self.commit()

