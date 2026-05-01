"""Add check constraints to distribution entries

Revision ID: 9cf8a18ce3c3
Revises: 62075f9a5761
Create Date: 2026-05-01 14:10:12.164285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cf8a18ce3c3'
down_revision = '62075f9a5761'
branch_labels = None
depends_on = None


def upgrade():
    op.create_check_constraint(
        "ck_distribution_entries_day_off_count_non_negative",
        "distribution_entries",
        "day_off_count >= 0"
    )
    op.create_check_constraint(
        "ck_distribution_entries_absence_count_non_negative",
        "distribution_entries",
        "absence_count >= 0"
    )
    op.create_check_constraint(
        "ck_distribution_entries_worked_days_non_negative",
        "distribution_entries",
        "worked_days >= 0"
    )
    op.create_check_constraint(
        "ck_distribution_entries_computed_hours_non_negative",
        "distribution_entries",
        "computed_hours >= 0"
    )
    op.create_check_constraint(
        "ck_distribution_entries_exact_amount_non_negative",
        "distribution_entries",
        "exact_amount >= 0"
    )
    op.create_check_constraint(
        "ck_distribution_entries_rounded_amount_non_negative",
        "distribution_entries",
        "rounded_amount >= 0"
    )
    op.create_check_constraint(
        "ck_distribution_entries_avg_hours_snapshot_positive",
        "distribution_entries",
        "average_daily_hours_snapshot > 0"
    )


def downgrade():
    op.drop_constraint("ck_distribution_entries_avg_hours_snapshot_positive", "distribution_entries", type_="check")
    op.drop_constraint("ck_distribution_entries_rounded_amount_non_negative", "distribution_entries", type_="check")
    op.drop_constraint("ck_distribution_entries_exact_amount_non_negative", "distribution_entries", type_="check")
    op.drop_constraint("ck_distribution_entries_computed_hours_non_negative", "distribution_entries", type_="check")
    op.drop_constraint("ck_distribution_entries_worked_days_non_negative", "distribution_entries", type_="check")
    op.drop_constraint("ck_distribution_entries_absence_count_non_negative", "distribution_entries", type_="check")
    op.drop_constraint("ck_distribution_entries_day_off_count_non_negative", "distribution_entries", type_="check")
