from marshmallow import Schema, fields


class CatalogSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.Str(dump_only=True)
    filepath = fields.Str(dump_only=True)
