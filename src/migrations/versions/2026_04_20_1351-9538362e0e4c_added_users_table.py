"""added users table

Revision ID: 9538362e0e4c
Revises: ea4aa5bc992a
Create Date: 2026-04-20 13:51:58.648089

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "9538362e0e4c"
down_revision: Union[str, Sequence[str], None] = "ea4aa5bc992a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=True),
        sa.Column("last_name", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
