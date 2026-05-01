from datetime import datetime
from app.extensions import db


class Distribution(db.Model):
    __tablename__ = "distributions"

    id = db.Column(db.Integer, primary_key=True)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    total_computed_hours = db.Column(db.Numeric(8, 2), nullable=False)
    total_tip_amount = db.Column(db.Numeric(10, 4), nullable=False)
    tip_per_hour = db.Column(db.Numeric(10, 4), nullable=False)

    total_exact_amount = db.Column(db.Numeric(10, 4), nullable=False)
    total_rounded_amount = db.Column(db.Numeric(10, 4), nullable=False)
    remainder_amount = db.Column(db.Numeric(10, 4), nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    __table_args__ = (
        db.CheckConstraint("end_date >= start_date"),
        db.CheckConstraint("total_computed_hours > 0"),
        db.CheckConstraint("total_tip_amount >= 0"),
        db.CheckConstraint("tip_per_hour >= 0"),
        db.CheckConstraint("total_exact_amount >= 0"),
        db.CheckConstraint("total_rounded_amount >= 0"),
        db.CheckConstraint("remainder_amount >= 0"),
    )


    def __repr__(self):
        return f"<Distribution {self.start_date} - {self.end_date}>"