from datetime import timedelta
from decimal import Decimal, ROUND_DOWN

from app.models import Absence, Employee, EmployeeDayOff


def daterange(start_date, end_date):
    current_date = start_date

    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)


def round_down_to_nearest_five(amount):
    amount = Decimal(amount)
    return (amount / Decimal("5")).to_integral_value(rounding=ROUND_DOWN) * Decimal("5")


def calculate_distribution(user_id, start_date, end_date, total_tip_amount):
    employees = Employee.query.filter_by(
        user_id=user_id,
        is_active=True,
    ).order_by(Employee.id.asc()).all()

    if not employees:
        raise ValueError("No employees found for this user")

    period_days = list(daterange(start_date, end_date))
    total_days = len(period_days)

    results = []
    total_computed_hours = Decimal("0.00")

    for employee in employees:
        day_offs = EmployeeDayOff.query.filter_by(employee_id=employee.id).all()
        day_off_weekdays = {day_off.weekday for day_off in day_offs}

        day_off_count = sum(
            1 for day in period_days
            if day.strftime("%A") in day_off_weekdays
        )

        absences = Absence.query.filter(
            Absence.employee_id == employee.id,
            Absence.date >= start_date,
            Absence.date <= end_date,
        ).all()

        valid_absence_count = sum(
            1 for absence in absences
            if absence.date.strftime("%A") not in day_off_weekdays
        )

        worked_days = total_days - day_off_count - valid_absence_count

        if worked_days < 0:
            worked_days = 0

        computed_hours = Decimal(worked_days) * employee.average_daily_hours
        total_computed_hours += computed_hours

        results.append({
            "employee_id": employee.id,
            "name": employee.name,
            "surname": employee.surname,
            "average_daily_hours_snapshot": employee.average_daily_hours,
            "day_off_count": day_off_count,
            "absence_count": valid_absence_count,
            "worked_days": worked_days,
            "computed_hours": computed_hours,
        })

    if total_computed_hours <= 0:
        raise ValueError("Total computed hours must be greater than 0")

    total_tip_amount = Decimal(str(total_tip_amount))
    tip_per_hour = total_tip_amount / total_computed_hours

    total_exact_amount = Decimal("0.0000")
    total_rounded_amount = Decimal("0.0000")

    for result in results:
        exact_amount = result["computed_hours"] * tip_per_hour
        rounded_amount = round_down_to_nearest_five(exact_amount)

        result["exact_amount"] = exact_amount
        result["rounded_amount"] = rounded_amount

        total_exact_amount += exact_amount
        total_rounded_amount += rounded_amount

    remainder_amount = total_tip_amount - total_rounded_amount

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_tip_amount": total_tip_amount,
        "total_computed_hours": total_computed_hours,
        "tip_per_hour": tip_per_hour,
        "total_exact_amount": total_exact_amount,
        "total_rounded_amount": total_rounded_amount,
        "remainder_amount": remainder_amount,
        "entries": results,
    }
