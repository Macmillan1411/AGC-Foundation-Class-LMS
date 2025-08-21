"""add is_admin to users

Revision ID: 39ed81d48e04
Revises: 4cbea4242cc2
Create Date: 2025-08-21 12:44:09.544769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39ed81d48e04'
down_revision: Union[str, Sequence[str], None] = '4cbea4242cc2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
