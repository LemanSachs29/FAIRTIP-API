from app.extensions import db


class EmployeeDayOff(db.Model):
    __tablename__ = "employee_day_offs"

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False
    )

    weekday = db.Column(
        db.String(15),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "employee_id",
            "weekday",
            name="uq_employee_day_offs_employee_weekday"
        ),
        db.CheckConstraint(
            "weekday IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')",
            name="ck_employee_day_offs_weekday_valid"
        ),
    )
    
    def __repr__(self):
        return f"<DayOff {self.weekday} for employee {self.employee_id}>"