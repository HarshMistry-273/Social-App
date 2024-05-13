"""Add Likes Table

Revision ID: 7c4cff0c8092
Revises: 9d609c5c9af3
Create Date: 2024-04-15 16:36:11.420851

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c4cff0c8092'
down_revision: Union[str, None] = '9d609c5c9af3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('likes', sa.Column('id', sa.String, primary_key=True, default=uuid.uuid4),
                    sa.Column('pid', sa.String, sa.ForeignKey('posts.id')),
                    sa.Column('uid', sa.String, sa.ForeignKey('users.id')))


def downgrade() -> None:
    op.drop_table('likes')
