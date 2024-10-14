# schemas.py
from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Str()
    title = fields.Str(required=True)
    description = fields.Str(required=True)
