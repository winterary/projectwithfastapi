"""add content column to posts table

Revision ID: df2daaae37bd
Revises: 45c0d0f1a17b
Create Date: 2025-04-05 22:49:38.223279

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df2daaae37bd'
down_revision: Union[str, None] = '45c0d0f1a17b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
