from marshmallow import Schema, fields
from marshmallow.validate import Range
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


class ProductSearchSchema(Schema):
    q = fields.Str(load_only=True, required=True)
    page = fields.Integer(load_only=True, validate=Range(min=1, error="Page value must be greater than 0"))
    rows = fields.Integer(load_only=True, validate=Range(min=1, error="Rows value must be greater than 0"))
    sort = fields.Str(load_only=True)


class ProductPaginationSchema(Schema):
    total = fields.Integer(dump_only=True)
    products = fields.List(fields.Nested(PlainProductSchema()), dump_only=True)
