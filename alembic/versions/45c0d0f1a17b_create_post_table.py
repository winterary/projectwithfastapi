"""create post table

Revision ID: 45c0d0f1a17b
Revises: 
Create Date: 2025-04-05 22:14:51.582138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45c0d0f1a17b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
    sa.Column("title", sa.String(), nullable=False))

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
    pass
