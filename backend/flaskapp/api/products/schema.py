from marshmallow import Schema, fields
from marshmallow.validate import Range


class PaginationSchema(Schema):
    page = fields.Integer(load_only=True, validate=Range(min=1, error="Page value must be greater than 0"), load_default=1)
    rows = fields.Integer(load_only=True, validate=Range(min=1, error="Rows value must be greater than 0"))
    sort = fields.Str(load_only=True)


class PlainProductSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(dump_only=True)
    availability = fields.Boolean(dump_only=True)
    productDescription = fields.Str(dump_only=True)
    imageURL = fields.Str(dump_only=True)
    price = fields.Float(dump_only=True)


class SearchSchema(PaginationSchema):
    q = fields.Str(load_only=True, required=True)


class ProductListSchema(Schema):
    total = fields.Integer(dump_only=True)
    rows = fields.Integer(dump_only=True)
    products = fields.List(fields.Nested(PlainProductSchema()), dump_only=True)
