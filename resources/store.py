from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store_model import StoreModel


class Store(Resource):
    TABLE_NAME = 'stores'

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store: 
            return store.json(), 200
        return {'Message': "Store '{}' cannot be found".format(name)}, 404

    def post(self, name):
        if StoreModel.find_by_name(name): 
            return {'Message': "Store '{}' already existed".format(name)},400   
        store = StoreModel(name)
        store.save_to_db()
        return {'Message': "Store '{}' was created sucessfuly".format(name)}, 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store: 
            store.delete_from_db()
            return {'Message': "Store '{}' was deleted sucessfully".format(name)},201 
        return {'Message': "Store '{}' does not exist".format(name)}, 404


class StoreList(Resource):

    def get(self):
        return {'Stores': [store.json() for store in StoreModel.query.all()]}, 200