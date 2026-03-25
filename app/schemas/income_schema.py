from marshmallow import Schema, ValidationError, fields, validates


class IncomeCreateSchema(Schema):
    amount = fields.Decimal(required=True, as_string=True)
    description = fields.Str(load_default=None)
    received_at = fields.DateTime(required=True)

    @validates("amount")
    def validate_amount(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("amount deve ser maior que zero")


class IncomeUpdateSchema(Schema):
    amount = fields.Decimal(load_default=None, as_string=True)
    description = fields.Str(load_default=None)
    received_at = fields.DateTime(load_default=None)

    @validates("amount")
    def validate_amount(self, value, **kwargs):
        if value is not None and value <= 0:
            raise ValidationError("amount deve ser maior que zero")


class IncomeOutputSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    amount = fields.Decimal(as_string=True, dump_only=True)
    description = fields.Str(dump_only=True)
    received_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
