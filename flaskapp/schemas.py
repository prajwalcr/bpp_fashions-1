from marshmallow import Schema, fields


class PlainProductSchema(Schema):
    id = fields.Str(dump_only=True, required=True)
    title = fields.Str(dump_only=True)
    availability = fields.Boolean(dump_only=True)
    productDescription = fields.Str(dump_only=True)
    imageURL = fields.Str(dump_only=True)
    price = fields.Float(dump_only=True, required=True)

