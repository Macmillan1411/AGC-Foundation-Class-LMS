"""add is_admin field

Revision ID: e351d3ed65e9
Revises: 39ed81d48e04
Create Date: 2025-08-21 13:32:22.955849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e351d3ed65e9'
down_revision: Union[str, Sequence[str], None] = '39ed81d48e04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
