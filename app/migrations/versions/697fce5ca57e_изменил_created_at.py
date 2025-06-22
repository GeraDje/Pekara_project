"""изменил created at

Revision ID: 697fce5ca57e
Revises: 256de5cb1068
Create Date: 2025-06-22 14:33:43.876180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '697fce5ca57e'
down_revision: Union[str, None] = '256de5cb1068'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
