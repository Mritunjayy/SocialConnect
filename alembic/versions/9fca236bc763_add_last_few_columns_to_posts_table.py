"""add last few columns to posts table

Revision ID: 9fca236bc763
Revises: 2ea34cb630a3
Create Date: 2024-07-19 04:17:27.322397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fca236bc763'
down_revision: Union[str, None] = '2ea34cb630a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable= False, server_default='True'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable= False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column("posts","published")
    pass
