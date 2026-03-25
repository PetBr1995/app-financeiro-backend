from marshmallow import Schema, ValidationError, fields, validates


class ExpenseCreateSchema(Schema):
    category_id = fields.Int(required=True)
    amount = fields.Decimal(required=True, as_string=True)
    description = fields.Str(load_default=None)
    spent_at = fields.DateTime(required=True)

    @validates("amount")
    def validate_amount(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("amount deve ser maior que zero")


class ExpenseUpdateSchema(Schema):
    category_id = fields.Int(load_default=None)
    amount = fields.Decimal(load_default=None, as_string=True)
    description = fields.Str(load_default=None)
    spent_at = fields.DateTime(load_default=None)

    @validates("amount")
    def validate_amount(self, value, **kwargs):
        if value is not None and value <= 0:
            raise ValidationError("amount deve ser maior que zero")


class ExpenseOutputSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    category_id = fields.Int(dump_only=True)
    amount = fields.Decimal(as_string=True, dump_only=True)
    description = fields.Str(dump_only=True)
    spent_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
