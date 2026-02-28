"""base

Revision ID: 2f8e5eabd3ab
Revises: e776d0b6f336
Create Date: 2026-02-26 23:03:14.155388

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f8e5eabd3ab'
down_revision: Union[str, Sequence[str], None] = 'e776d0b6f336'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
