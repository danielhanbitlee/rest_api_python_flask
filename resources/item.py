from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# every api works with resources. and every resource has to be a class.
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True, # this makes sure that no request can come through with no price
        help = "This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type = int,
        required = True, # this makes sure that no request can come through with no price
        help = "Every item needs a store id."
    )

    @jwt_required() # ths means that we have to authenticate before we call the get method
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        # data = request.get_json() # data is going to be a dictionary
        # force = True parameter in requests.get_json() means that you do not need the content-type header.
        # it will just look in the content and it will format it even if the content-type header is not set to be application/json
        # this is nice, but is also dangerous because it measn that without force = true, if the header is not set correctly, you just do nothing
        # with force = True, you don't look at the header. therefore you're always going to be doing the processing of the text even if it is incorrect.
        # i tend to not use force = True.
        # silent = True parameter in requests.get_json(). this doesn't give an error. it returns none.
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 # internal server error

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        # initialize a new object, which we can use to parse the request.
        # we are going to run the request through it and see what arguments
        # match those that we defined in the parser.

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # return {'items': [item.json() for item in ItemModel.query.all()]} this is using list comprehension
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
