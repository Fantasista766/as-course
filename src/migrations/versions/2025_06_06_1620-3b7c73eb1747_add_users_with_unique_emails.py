"""add users with unique emails

Revision ID: 3b7c73eb1747
Revises: 7ee8acac53cb
Create Date: 2025-06-06 16:20:43.655331

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3b7c73eb1747"
down_revision: Union[str, None] = "7ee8acac53cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
