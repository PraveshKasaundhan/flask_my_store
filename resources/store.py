
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from schemas import StoreSchema, UpdateStoreSchema
from models import StoreModel
from db import db

blp = Blueprint("Stores",__name__,description="APIs on Store")


@blp.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self,store_data):
        store=StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="DB Error")
        return store


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @jwt_required()
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    @blp.arguments(UpdateStoreSchema)
    @blp.response(201,StoreSchema)
    def put(self,store_data,store_id):
        store = StoreModel.query.get(store_id)
        if store:
            store.name=store_data['name']
        else:
            store=StoreModel(id=store_id,**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="DB Error")
        return store

    @jwt_required(fresh=True)
    def delete(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400,str(e))
        return {'msg':'Deleted'}

