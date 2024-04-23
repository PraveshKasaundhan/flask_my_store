from os import getenv
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from blocklist import BLOCKLIST

from resources.item import blp as ItemBlp
from resources.store import blp as StoreBlp
from resources.tag import blp as TagBlp
from resources.user import blp as UserBlp

def create_app(db_url=None):
    load_dotenv()

    app=Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "My Stores REST API"
    app.config["API_VERSION"] = "v1"

    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

    app.config['JWT_SECRET_KEY']=getenv("JWT_SECRET_KEY","1234567890")

    db.init_app(app)
    migrate=Migrate(app,db)
    # with app.app_context():
    #     db.create_all()


    jwt = JWTManager(app)

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header,jwt_payload):
        return (jsonify({"msg":"Need Fresh Token","error":"need_fresh_token"}),401)

    @jwt.token_in_blocklist_loader
    def check_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwtheader,jwt_payload):
        return (jsonify({"msg":"Token Revoked","error":"token_revoked"}),401)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if isinstance(identity, int):
            return {"good_user":True}
        return {"good_user":False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_payload):
        return (jsonify({"msg":"Token Expired","error":"token_expired"}),401)
    
    @jwt.invalid_token_loader
    def expired_token_callback(error):
        return (jsonify({"msg":"Token Invalid","error":"token_invalid"}),401)
    
    @jwt.unauthorized_loader
    def expired_token_callback(error):
        return (jsonify({"msg":"Login Required","error":"token_required"}),401)
    


    api=Api(app)
    api.register_blueprint(StoreBlp)
    api.register_blueprint(ItemBlp)
    api.register_blueprint(TagBlp)
    api.register_blueprint(UserBlp)


    return app