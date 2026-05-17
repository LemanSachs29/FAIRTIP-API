"""Add is_active to employees

Revision ID: 4f4a24f4a0f7
Revises: 331be1928fa6
Create Date: 2026-05-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f4a24f4a0f7'
down_revision = '331be1928fa6'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.add_column(sa.Column(
            'is_active',
            sa.Boolean(),
            server_default=sa.true(),
            nullable=False
        ))


def downgrade():
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_column('is_active')
