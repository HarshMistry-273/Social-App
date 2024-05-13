"""Create follow table

Revision ID: 51df69f52e1d
Revises: 39538a353812
Create Date: 2024-04-16 15:03:38.795387

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51df69f52e1d'
down_revision: Union[str, None] = '39538a353812'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('follows', sa.Column('id', sa.String, primary_key=True, default=uuid.uuid4),
                    sa.Column('follower_id', sa.String,  sa.ForeignKey('users.id')),
                    sa.Column('following_id', sa.String,  sa.ForeignKey('users.id')))


def downgrade() -> None:
    op.drop_table('follows')
