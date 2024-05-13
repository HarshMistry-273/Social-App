"""Add Comments Table

Revision ID: de1afd33f779
Revises: 7c4cff0c8092
Create Date: 2024-04-15 16:36:21.395079

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa



revision: str = 'de1afd33f779'
down_revision: Union[str, None] = '7c4cff0c8092'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('comments', sa.Column('id', sa.String, primary_key=True, default= uuid.uuid4),
                    sa.Column('comm',sa.String),
                    sa.Column('pid', sa.ForeignKey('posts.id')),
                    sa.Column('uid', sa.ForeignKey('users.id')),
                    sa.Column('done_at', sa.DateTime, default=sa.func.now())
                    )

def downgrade() -> None:
    op.drop_table('comments')
