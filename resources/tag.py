
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import StoreModel, TagModel, ItemModel
from schemas import TagSchema, UpdateTagSchema

blp=Blueprint("Tags",__name__,description="APIs on Tag")

    
@blp.route("/tag")
class TagList(MethodView):
    @jwt_required()
    @blp.response(200,TagSchema(many=True))
    def get(self):
        return TagModel.query.all()

@blp.route("/store/<int:store_id>/tag")
class TagInStore(MethodView):
    @jwt_required()
    @blp.response(200,TagSchema(many=True))
    def get(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @jwt_required()
    @blp.arguments(UpdateTagSchema)
    @blp.response(201,TagSchema)
    def post(self,tag_data,store_id):
        tag=TagModel(**tag_data,store_id=store_id)
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data['name']).first():
            abort(400,message="Duplicate Request")
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,str(e))
        return tag

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @jwt_required()
    @blp.response(200,TagSchema)
    def get(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        return tag
    
    @jwt_required()
    @blp.arguments(UpdateTagSchema)
    @blp.response(201,TagSchema)
    def put(self,tag_data,tag_id):
        tag=TagModel.query.get(tag_id)
        if tag:
            tag.name=tag_data['name']
        else:
            tag=TagModel(**tag_data,id=tag_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,str(e))
        return tag
    
    @jwt_required(fresh=True)
    def delete(self,tag_id):
        tag= TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"msg":"Tag Deleted"}
        abort(400,message="Restricted by Items")
        
    

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class ItemsTagsLink(MethodView):
    @jwt_required()
    @blp.response(200,TagSchema)
    def post(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        if item.store_id != tag.store_id:
            abort(400,messsage="Invalid Request")
        
        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,str(e))
        return tag
    
    @jwt_required(fresh=True)
    def delete(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        if item.store_id != tag.store_id:
            abort(400,messsage="Invalid Request")
        
        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,str(e))
        return {"msg":"Mapping Unlinked"}