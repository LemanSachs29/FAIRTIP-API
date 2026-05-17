"""Add check constraints to employee day offs

Revision ID: ae38612375d5
Revises: 7c224c59e9c1
Create Date: 2026-05-01 13:55:34.275910

"""
from alembic import op
import sqlalchemy as sa


revision = 'ae38612375d5'
down_revision = '7c224c59e9c1'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "postgresql":
        with op.batch_alter_table('employee_day_offs', schema=None) as batch_op:
            batch_op.drop_constraint(
                batch_op.f('employee_day_offs_employee_id_weekday_key'),
                type_='unique'
            )
            batch_op.create_unique_constraint(
                'uq_employee_day_offs_employee_weekday',
                ['employee_id', 'weekday']
            )

    elif dialect == "mysql":
        # MySQL already has the UNIQUE constraint from the original table creation.
        # We skip renaming it because MySQL may not use the PostgreSQL constraint name.
        pass

    else:
        pass


def downgrade():
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "postgresql":
        with op.batch_alter_table('employee_day_offs', schema=None) as batch_op:
            batch_op.drop_constraint(
                'uq_employee_day_offs_employee_weekday',
                type_='unique'
            )
            batch_op.create_unique_constraint(
                batch_op.f('employee_day_offs_employee_id_weekday_key'),
                ['employee_id', 'weekday'],
                postgresql_nulls_not_distinct=False
            )

    elif dialect == "mysql":
        pass

    else:
        pass