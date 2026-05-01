"""Add check constraints to distributions

Revision ID: 62075f9a5761
Revises: ae38612375d5
Create Date: 2026-05-01 14:03:08.559368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62075f9a5761'
down_revision = 'ae38612375d5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_check_constraint(
        "ck_distributions_end_date_after_start_date",
        "distributions",
        "end_date >= start_date"
    )
    op.create_check_constraint(
        "ck_distributions_total_computed_hours_positive",
        "distributions",
        "total_computed_hours > 0"
    )
    op.create_check_constraint(
        "ck_distributions_total_tip_amount_non_negative",
        "distributions",
        "total_tip_amount >= 0"
    )
    op.create_check_constraint(
        "ck_distributions_tip_per_hour_non_negative",
        "distributions",
        "tip_per_hour >= 0"
    )
    op.create_check_constraint(
        "ck_distributions_total_exact_amount_non_negative",
        "distributions",
        "total_exact_amount >= 0"
    )
    op.create_check_constraint(
        "ck_distributions_total_rounded_amount_non_negative",
        "distributions",
        "total_rounded_amount >= 0"
    )
    op.create_check_constraint(
        "ck_distributions_remainder_amount_non_negative",
        "distributions",
        "remainder_amount >= 0"
    )

def downgrade():
    op.drop_constraint("ck_distributions_remainder_amount_non_negative", "distributions", type_="check")
    op.drop_constraint("ck_distributions_total_rounded_amount_non_negative", "distributions", type_="check")
    op.drop_constraint("ck_distributions_total_exact_amount_non_negative", "distributions", type_="check")
    op.drop_constraint("ck_distributions_tip_per_hour_non_negative", "distributions", type_="check")
    op.drop_constraint("ck_distributions_total_tip_amount_non_negative", "distributions", type_="check")
    op.drop_constraint("ck_distributions_total_computed_hours_positive", "distributions", type_="check")
    op.drop_constraint("ck_distributions_end_date_after_start_date", "distributions", type_="check")