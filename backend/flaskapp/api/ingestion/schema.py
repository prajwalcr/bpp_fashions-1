from marshmallow import Schema
from flask_smorest.fields import Upload


class MultiPartFileSchema(Schema):
    """Schema class for validating file upload requests."""
    file = Upload(load_only=True, required=True)
