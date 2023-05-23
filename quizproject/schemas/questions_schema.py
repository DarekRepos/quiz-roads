
from marshmallow import Schema, fields


class QuestionSchema(Schema):
    id = fields.Integer()
    text = fields.String()
    from_quiz = fields.Dict()
    difficulty = fields.Integer()
    multi_answer = fields.Boolean()
    is_active = fields.Boolean()
    


    # description = fields.Str()
    # amount = fields.Number()
    # created_at = fields.Date()
    # type = fields.Str()