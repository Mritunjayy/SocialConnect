"""add content column to posts table

Revision ID: 8afa18ca8fb0
Revises: 7f55d40bcd17
Create Date: 2024-07-19 04:12:17.746264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8afa18ca8fb0'
down_revision: Union[str, None] = '7f55d40bcd17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
