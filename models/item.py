import sqlite3
from db import db


class ItemModel(db.Model): # internal representation of item, so it has to contain properites of item as object properties
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel') # so every itemmodel has a property store that is the store which matches the store_id
                                          # store is one store that the item belongs to

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self): # this fn returns json representation of the model
        return {'name': self.name, 'price': self.price}

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
