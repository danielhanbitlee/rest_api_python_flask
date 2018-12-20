import sqlite3
from db import db


class StoreModel(db.Model): # internal representation of item, so it has to contain properites of item as object properties
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy = 'dynamic') # this is a list of item models bc a store can have more than one items

    def __init__(self, name):
        self.name = name

    def json(self): # this fn returns json representation of the model
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first() # Select * FROM items WHERE name = name LIMIT 1

    def save_to_db(self):
        # this method does both insert and update
        db.session.add(self) # session in this instance is the collection of objects that we're going to write to the database
                             # we can also add multiple objects to the session and then write them all at once
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
