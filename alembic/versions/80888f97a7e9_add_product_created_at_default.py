"""add product created_at default

Revision ID: 80888f97a7e9
Revises: 7da7bbf746b4
Create Date: 2026-09-28 21:06:47.339507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80888f97a7e9'
down_revision: Union[str, Sequence[str], None] = '7da7bbf746b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "products",
        "created_at",
        existing_type=sa.DateTime(),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "products",
        "created_at",
        existing_type=sa.DateTime(),
        server_default=None,
        existing_nullable=False,
    )
