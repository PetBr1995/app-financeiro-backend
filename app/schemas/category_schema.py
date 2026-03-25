from marshmallow import Schema, fields


class CategoryCreateSchema(Schema):
    name = fields.Str(required=True)


class CategoryUpdateSchema(Schema):
    name = fields.Str(required=True)


class CategoryOutputSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
