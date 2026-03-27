"""add password reset tokens

Revision ID: 8c6f7d9a1234
Revises: 2f1828e7f114
Create Date: 2026-03-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8c6f7d9a1234"
down_revision = "2f1828e7f114"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "password_reset_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("password_reset_tokens", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_password_reset_tokens_user_id"), ["user_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_password_reset_tokens_token_hash"), ["token_hash"], unique=True)
        batch_op.create_index(batch_op.f("ix_password_reset_tokens_expires_at"), ["expires_at"], unique=False)


def downgrade():
    with op.batch_alter_table("password_reset_tokens", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_password_reset_tokens_expires_at"))
        batch_op.drop_index(batch_op.f("ix_password_reset_tokens_token_hash"))
        batch_op.drop_index(batch_op.f("ix_password_reset_tokens_user_id"))

    op.drop_table("password_reset_tokens")
