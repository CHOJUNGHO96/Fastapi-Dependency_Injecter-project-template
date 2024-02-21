"""user_info table

Revision ID: be5f0acdce0a
Revises: 
Create Date: 2024-02-21 17:50:16.729849

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "be5f0acdce0a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_info",
        sa.Column("user_id", sa.Integer(), sa.Identity(), nullable=False),
        sa.Column("login_id", sa.VARCHAR(255), nullable=False),
        sa.Column("user_password", sa.VARCHAR(255), nullable=False),
        sa.Column("user_email", sa.VARCHAR(255), nullable=False),
        sa.Column("user_name", sa.VARCHAR(255), nullable=False),
        sa.Column("is_enable", sa.Integer(), server_default="1", nullable=False),
        sa.Column("reg_date", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("user_id", name=op.f("user_info_pkey")),
    )

    op.create_index(
        "user_info_login_id_key",
        "user_info",
        ["login_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_table("user_info")
