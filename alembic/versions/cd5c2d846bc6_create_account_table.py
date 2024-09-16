"""create account table

Revision ID: cd5c2d846bc6
Revises: 7cbfe5b47316
Create Date: 2024-09-09 10:54:49.783533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd5c2d846bc6'
down_revision: Union[str, None] = '7cbfe5b47316'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
