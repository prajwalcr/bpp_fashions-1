from marshmallow import Schema, fields


class CatalogSchema(Schema):
    """Schema class for validating catalog data response."""
    id = fields.Int(dump_only=True)
    status = fields.Str(dump_only=True)
    filepath = fields.Str(dump_only=True)
