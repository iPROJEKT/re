"""init mat

Revision ID: ea860b32224d
Revises: 4f7a42438a07
Create Date: 2024-08-19 16:24:16.777542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea860b32224d'
down_revision: Union[str, None] = '4f7a42438a07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mudguard', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mudguard_material', sa.String(), nullable=False))
        batch_op.drop_column('mudguard_matireal')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mudguard', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mudguard_matireal', sa.VARCHAR(), nullable=False))
        batch_op.drop_column('mudguard_material')

    # ### end Alembic commands ###
