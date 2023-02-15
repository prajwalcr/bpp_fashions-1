from marshmallow import Schema
from flask_smorest.fields import Upload


class MultiPartFileSchema(Schema):
    file = Upload(load_only=True, required=True)
