
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from schemas import ItemSchema, UpdateItemSchema
from models import ItemModel
from db import db

blp = Blueprint("Items",__name__,description="APIs on Item")


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200,ItemSchema)
    def post(self,item_data):
        item = ItemModel(**item_data)
        if ItemModel.query.filter(ItemModel.store_id == item_data['store_id'], ItemModel.name== item_data['name']).first():
            abort(500,message="Duplicate Request")
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="DB Error")
        return item


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        item=ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    @blp.arguments(UpdateItemSchema)
    @blp.response(201,ItemSchema)
    def put(self,item_data,item_id):
        item=ItemModel.query.get(item_id)
        if item:
            item.name=item_data['name']
            item.price=item_data['price']
        else:
            item=ItemModel(**item_data,id=item_id)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="DB Error")
        return item

    @jwt_required(fresh=True)
    def delete(self,item_id):
        item=ItemModel.query.get_or_404(item_id)
        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400,str(e))
        return {'msg':'Item Deleted'}


