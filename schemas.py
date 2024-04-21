from marshmallow import Schema, fields

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Int(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class UpdateStoreSchema(Schema):
    name = fields.Str()

class UpdateItemSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

class UpdateTagSchema(Schema):
    name = fields.Str()
    store_id = fields.Int()


class StoreSchema(PlainStoreSchema):
    items=fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    tags=fields.List(fields.Nested(PlainTagSchema()),dump_only=True)

class ItemSchema(PlainItemSchema):
    store_id=fields.Int(required=True,load_only=True)
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    tags=fields.List(fields.Nested(PlainTagSchema()),dump_only=True)

class TagSchema(PlainTagSchema):
    store_id=fields.Int(required=True,load_only=True)
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    items=fields.List(fields.Nested(PlainItemSchema()),dump_only=True)

class ItemTagSchema(Schema):
    message=fields.Str()
    id=fields.Int()
    tag_id=fields.Nested(TagSchema())
    item_id=fields.Nested(ItemSchema())

class UserSchema(Schema):
    id=fields.Int(dump_only=True)
    username=fields.Str(required=True)
    password=fields.Str(required=True,load_only=True)