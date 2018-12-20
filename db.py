from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# we got an object, which is sqlalchemy. that is essentially a thing that is
# going to link to our Flask app. And it's going to look at all of the objects
# that we tell it to. and then it's going to allow us to map those objects
# to rows in a database.
# e.g. when we create an ItemModel object, that has a column called name
# and a column called price, it's going to allow us to very easily put that object
# into our database. Naturally, putting an object into a database, all that is is saving
# the object's properties into the database. and that's what sqlalchemy excels at.
