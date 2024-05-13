"""Create users table

Revision ID: 98f496eca55d
Revises: 
Create Date: 2024-04-15 09:35:31.966616

"""
from datetime import datetime
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98f496eca55d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.String, primary_key=True, default=uuid.uuid4),
                    sa.Column('full_name', sa.String),
                    sa.Column('email', sa.String, unique=True),
                    sa.Column('phno', sa.String, unique=True),
                    sa.Column('username',sa.String, unique=True),
                    sa.Column('password', sa.String),
                    sa.Column('created_at', sa.DateTime, default=sa.func.now()),
                    sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now()),
                    sa.Column('is_verified', sa.Boolean, default=False)
                    )


def downgrade() -> None:
    op.drop_table('users')
