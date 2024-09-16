"""table

Revision ID: 546ba0f054c3
Revises: cd5c2d846bc6
Create Date: 2024-09-09 10:57:12.642262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '546ba0f054c3'
down_revision: Union[str, None] = 'cd5c2d846bc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'table',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('shift_responsible', sa.String(), nullable=True)
    )


def downgrade():
    op.drop_table('table')
