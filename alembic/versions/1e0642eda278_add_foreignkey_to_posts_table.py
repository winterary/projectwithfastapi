"""add foreignkey to posts table

Revision ID: 1e0642eda278
Revises: 9619065dd8b9
Create Date: 2025-04-05 23:04:38.576850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e0642eda278'
down_revision: Union[str, None] = '9619065dd8b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',local_cols=["owner_id"], remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint ('post_user_fk', table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
