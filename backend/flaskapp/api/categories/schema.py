from marshmallow import Schema, fields


class CategorySchema(Schema):
    """Schema class for validating category data response."""
    id = fields.Int(dump_only=True)
    parent_id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    level = fields.Int(dump_only=True)
