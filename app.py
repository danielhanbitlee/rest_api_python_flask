from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# what is Resource? A resource represents something that our api sort of represents.
# e.g. if our api is concerned with students, and it can return students and create students, a student would be a resource.
# e.g. if our api is concerned with items, then an item may be a resource.
# e.g. if our api is concerned with pianos, then a piano may be a resource.
# resources are usually mapped into database tables as well.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # this means that sqlalchemy database is going to live at the root folder of our project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # this turns off the flask sqlalchemy modification tracker. it does not turn off sqlalchemy modification tracker
app.secret_key = 'jose'
api = Api(app) # this allows us to very easily add these resources to it. we are going to be able to get and post a resource, get and delete a resource, get put post and delete another

jwt = JWT(app, authenticate, identity)
# jwt creates a new endpt /auth. when we call /auth, we send it a username and password.
# jwt extension gets that username and password and sends it over to the authenticate fn in security.py
# authenticte finds the correct user object using that username and compare the password to the one that we received thru the /auth endpt
# if they match, we are going to return the user. and the returned user is going to be that identity.
# then, the /auth endpt returns a JW token. this jw token in itself doesnt do anything.
# but we can send it to the next request we make.
# so when we send a jw token, what jwt does is it calls the identity fn and then it uses the jwt token to ge tthe user id
# and with that, it gets the correct user for that user id that the jwt toekn represents.
# and if it can do that, that means that the user was authenticated, the jwt token is valid, and all is good.

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__': # this is to prevent the following code to be run when importing
    from db import db
    db.init_app(app)
    app.run(port = 5000, debug = True)

# put request - ability to modify an existing item. post is used to send data to the server and gathers you with the data. put is used to give it to the server and then do one of two things:
# create a new item or update an existing item that already exists with that unique identifier.
