"""Add posts table

Revision ID: 9d609c5c9af3
Revises: 69528412f51a
Create Date: 2024-04-15 15:30:09.594859

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d609c5c9af3'
down_revision: Union[str, None] = '69528412f51a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.String, primary_key=True, default=uuid.uuid4),
                    sa.Column('title', sa.String),
                    sa.Column('content', sa.String),
                    sa.Column('uid', sa.String, sa.ForeignKey('users.id')),
                    sa.Column('created_at', sa.DateTime, default = sa.func.now()),
                    sa.Column('updated_at', sa.DateTime, onupdate = sa.func.now()),
                    sa.Column('like_cnt', sa.Integer, default=0),
                    sa.Column('comment_cnt', sa.Integer, default=0)
                    )


def downgrade() -> None:
    op.drop_table('posts')
