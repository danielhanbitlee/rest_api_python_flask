from app import app
from db import db

db.init_app(app)

# before the first request, no matter what the request is, app.py is going to run db.create_all()
# this is going to create sqlite:///data.db
# this will create all the files in data.db unless they already exist.
@app.before_first_request
def create_tables():
    db.create_all()
