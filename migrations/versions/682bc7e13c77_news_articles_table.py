"""news_articles table

Revision ID: 682bc7e13c77
Revises: be5f0acdce0a
Create Date: 2024-02-21 18:08:51.552423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "682bc7e13c77"
down_revision: Union[str, None] = "be5f0acdce0a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "news_articles",
        sa.Column("article_id", sa.Integer(), sa.Identity(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("source", sa.VARCHAR(100), nullable=False),
        sa.Column("url", sa.VARCHAR(255), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("is_enable", sa.Integer(), server_default="1", nullable=False),
        sa.Column("reg_date", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("article_id", name=op.f("news_articles_pkey")),
    )

    op.create_foreign_key(
        "fk_user_id",
        "news_articles",
        "user_info",
        ["user_id"],
        ["user_id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_table("user_info")
