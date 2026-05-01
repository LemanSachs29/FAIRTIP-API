from datetime import datetime
from app.extensions import db


class Absence(db.Model):
    __tablename__ = "absences"

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(
        db.Date,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint("employee_id", "date"),
    )

    def __repr__(self):
        return f"<Absence employee={self.employee_id} date={self.date}>"