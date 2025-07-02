"""unique hotels

Revision ID: f5116e03e1fc
Revises: 9961c9a1ec80
Create Date: 2025-07-02 16:22:20.895067

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f5116e03e1fc"
down_revision: Union[str, None] = "9961c9a1ec80"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint("hotels_location_key", "hotels", ["location"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("hotels_location_key"), "hotels", type_="unique")
