"""add content column to post table

Revision ID: 51f65b9a9a94
Revises: b8d0aa0b79fc
Create Date: 2023-12-07 12:03:19.577382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51f65b9a9a94'
down_revision: Union[str, None] = 'b8d0aa0b79fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
