"""Create OTP table

Revision ID: 69528412f51a
Revises: 98f496eca55d
Create Date: 2024-04-15 13:57:47.702523

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69528412f51a'
down_revision: Union[str, None] = '98f496eca55d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('otp', sa.Column('id', sa.String, primary_key =True, default = uuid.uuid4),
                    sa.Column('code', sa.String),
                    sa.Column('created_at', sa.DateTime, default= sa.func.now()),
                    sa.Column('email', sa.String)
                    )


def downgrade() -> None:
    op.drop_table('otp')
