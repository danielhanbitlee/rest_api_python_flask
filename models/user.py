import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True) # we are telling sqlalchemy that there is a column called id, which is of type integer, and it's a primary key
    username = db.Column(db.String(80)) # 80 limits the size of the username. it's an optional parameter
    password = db.Column(db.String(80))

    def __init__(self, username, password): #_id is used because id is a python keyword. we dont want to use id as a variable name.
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()
