from marshmallow import Schema, fields
from flask_smorest.fields import Upload


class PlainProductSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(dump_only=True)
    availability = fields.Boolean(dump_only=True)
    productDescription = fields.Str(dump_only=True)
    imageURL = fields.Str(dump_only=True)
    price = fields.Float(dump_only=True)


class MultiPartFileSchema(Schema):
    file = Upload(load_only=True, required=True)
