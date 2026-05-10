from app.extensions import db


class DistributionEntry(db.Model):
    __tablename__ = "distribution_entries"

    id = db.Column(db.Integer, primary_key=True)

    day_off_count = db.Column(db.Integer, nullable=False)
    absence_count = db.Column(db.Integer, nullable=False, default=0)
    worked_days = db.Column(db.Integer, nullable=False)

    computed_hours = db.Column(db.Numeric(8, 2), nullable=False)

    exact_amount = db.Column(db.Numeric(10, 4), nullable=False)
    rounded_amount = db.Column(db.Numeric(10, 4), nullable=False)

    average_daily_hours_snapshot = db.Column(db.Numeric(5, 2), nullable=False)

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False
    )

    distribution_id = db.Column(
        db.Integer,
        db.ForeignKey("distributions.id"),
        nullable=False
    )

    employee = db.relationship('Employee', backref='distribution_entries')

    __table_args__ = (
        db.UniqueConstraint(
            "distribution_id",
            "employee_id",
            name="uq_distribution_employee"
        ),
        db.CheckConstraint("day_off_count >= 0", name="ck_distribution_entries_day_off_count_non_negative"),
        db.CheckConstraint("absence_count >= 0", name="ck_distribution_entries_absence_count_non_negative"),
        db.CheckConstraint("worked_days >= 0", name="ck_distribution_entries_worked_days_non_negative"),
        db.CheckConstraint("computed_hours >= 0", name="ck_distribution_entries_computed_hours_non_negative"),
        db.CheckConstraint("exact_amount >= 0", name="ck_distribution_entries_exact_amount_non_negative"),
        db.CheckConstraint("rounded_amount >= 0", name="ck_distribution_entries_rounded_amount_non_negative"),
        db.CheckConstraint("average_daily_hours_snapshot > 0", name="ck_distribution_entries_avg_hours_snapshot_positive"),
    )

    def __repr__(self):
        return f"<DistributionEntry dist={self.distribution_id} emp={self.employee_id}>"