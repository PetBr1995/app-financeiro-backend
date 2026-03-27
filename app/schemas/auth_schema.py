from marshmallow import Schema, ValidationError, fields, validates


def validate_password_strength(value):
    if len(value) < 8:
        raise ValidationError("A senha deve ter no mínimo 8 caracteres")


class RegisterSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

    @validates("password")
    def validate_password(self, value, **kwargs):
        validate_password_strength(value)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True)


class ResetPasswordSchema(Schema):
    token = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

    @validates("password")
    def validate_password(self, value, **kwargs):
        validate_password_strength(value)


class UserOutputSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
