"""add user table

Revision ID: 9619065dd8b9
Revises: df2daaae37bd
Create Date: 2025-04-05 22:56:34.651701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9619065dd8b9'
down_revision: Union[str, None] = 'df2daaae37bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id',sa.Integer(), nullable = False),
    sa.Column('email', sa.String, nullable= False),
    sa.Column('password',sa.String, nullable = False),
    sa.Column( 'created_at', sa.TIMESTAMP(timezone = True), 
                    server_default = sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
    )   
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
