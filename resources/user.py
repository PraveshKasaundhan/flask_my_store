import requests
from os import getenv
from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required, get_jwt, get_jwt_identity

from tasks import send_user_register_email

from db import db
from models import UserModel
from schemas import UserSchema, UserRegisterSchema
from blocklist import BLOCKLIST

blp=Blueprint("Users",__name__,description="APIs on User")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self,user_data):
        user=UserModel(username=user_data['username'],email=user_data['email'],password=pbkdf2_sha256.hash(user_data['password']))
        try:
            db.session.add(user)
            db.session.commit()

            # current_app.queue.enqueue(send_user_register_email,user.email,user.username)
        
        except SQLAlchemyError as e:
            abort(500,str(e))
        return {"msg":"User Created"}
    
    @blp.response(200,UserRegisterSchema(many=True))
    def get(self):
        return UserModel.query.all()


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        user= UserModel.query.filter(UserModel.username == user_data['username']).first()
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token=create_access_token(identity=user.id,fresh=True)
            refresh_token=create_refresh_token(identity=user.id)
            return {"access_token":access_token,"refresh_token":refresh_token}
        abort(400,message="Invalid Credentials")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_id=get_jwt_identity()
        new_token=create_access_token(identity=current_id,fresh=False)
        # Created non-fresh Token ONCE and destroyed the fresh token below.
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        print("OK",jti)
        print(BLOCKLIST)
        return {"access_token":new_token}
        

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"msg":"Logout Sucessfull"}



# Below routes are for testing only, should  be deleted
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200,UserRegisterSchema)
    def get(self, user_id):
        user=UserModel.query.get_or_404(user_id)
        return user

    def delete(self,user_id):
        user=UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,str(e))
        return {"msg":"User Deleted"}