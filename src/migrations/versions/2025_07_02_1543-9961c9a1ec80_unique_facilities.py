"""unique facilities

Revision ID: 9961c9a1ec80
Revises: 028325079833
Create Date: 2025-07-02 15:43:58.384644

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa: F401


revision: str = "9961c9a1ec80"
down_revision: Union[str, None] = "028325079833"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "facilities", ["title"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "facilities", type_="unique")  # type: ignore
