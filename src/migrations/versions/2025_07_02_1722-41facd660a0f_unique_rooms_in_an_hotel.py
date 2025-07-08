"""unique rooms in an hotel

Revision ID: 41facd660a0f
Revises: f5116e03e1fc
Create Date: 2025-07-02 17:22:27.546941

"""

from typing import Sequence, Union

from alembic import op


revision: str = "41facd660a0f"
down_revision: Union[str, None] = "f5116e03e1fc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint("uq_title_location", "rooms", ["hotel_id", "title"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_title_location", "rooms", type_="unique")
