import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from model import Base, Project, Category, Task
from . import Backend
import config

class DB(Backend):
    def __init__(self, engine):
        engine = create_engine(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
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
            Base.metadata.create_all(self.session.bind)
        except OperationalError:
            print('Cannot create DB %s' % config.engine)

    def drop(self):
        try:
            Base.metadata.drop_all(self.session.bind)
        except OperationalError:
            print('Cannot drop DB %s' % config.engine)

    def reset(self):
        for table in (Project, Category, Task):
            if table.__table__.exists(self.session.bind):
                self.session.connection().execute(table.__table__.delete())
        self.commit()

    def apply_filter(self, query, flt):
        if flt is not None:
            for col, val in flt.items():
                query = query.filter(col == val)

        return query

    def item_exists(self, cls, flt = None):
        query = self.session.query(cls)
        query = self.apply_filter(query, flt)

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
        query = self.apply_filter(query, flt)
        return query.all()

    def get_item(self, cls, flt = None):
        results = self.get_items(cls, flt)
        if len(results) == 1:
            return results[0]
        else:
            return None

    def bulk_update(self, cls, changes, flt = None):
        query = self.session.query(cls)
        query = self.apply_filter(query, flt)
        query.update(changes)
        self.commit()

