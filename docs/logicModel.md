# Fairtip Logical Database Model

## Overview

Fairtip is a restaurant tip distribution system built with Flask and PostgreSQL.

The database design focuses on:
- employee management,
- absences and weekly day offs,
- authenticated multi-user ownership,
- and tip distribution calculations.

---

# Tables

## users

Stores authenticated application users.

| Field | Type | Constraints |
|---|---|---|
| id | INT | PK |
| email | VARCHAR(255) | NOT NULL, UNIQUE |
| password_hash | VARCHAR(255) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL |

---

## employees

Stores employees managed by a user.

| Field | Type | Constraints |
|---|---|---|
| id | INT | PK |
| name | VARCHAR(100) | NOT NULL |
| surname | VARCHAR(200) | NOT NULL |
| average_daily_hours | DECIMAL(5,2) | NOT NULL, CHECK > 0 |
| created_at | TIMESTAMP | NOT NULL |
| updated_at | TIMESTAMP | NOT NULL |
| user_id | INT | FK → users(id), NOT NULL |

---

## employee_day_offs

Stores recurring weekly days off for employees.

| Field | Type | Constraints |
|---|---|---|
| id | INT | PK |
| employee_id | INT | FK → employees(id), NOT NULL |
| weekday | VARCHAR(15) | NOT NULL |

### Additional Constraints

- UNIQUE(employee_id, weekday)
- CHECK weekday IN:
  - Monday
  - Tuesday
  - Wednesday
  - Thursday
  - Friday
  - Saturday
  - Sunday

---

## absences

Stores individual employee absences.

| Field | Type | Constraints |
|---|---|---|
| id | INT | PK |
| date | DATE | NOT NULL |
| created_at | TIMESTAMP | NOT NULL |
| employee_id | INT | FK → employees(id), NOT NULL |

### Additional Constraints

- UNIQUE(employee_id, date)

---

## distributions

Stores generated tip distributions.

| Field | Type | Constraints |
|---|---|---|
| id | INT | PK |
| start_date | DATE | NOT NULL |
| end_date | DATE | NOT NULL |
| total_computed_hours | DECIMAL(8,2) | NOT NULL |
| total_tip_amount | DECIMAL(10,4) | NOT NULL |
| tip_per_hour | DECIMAL(10,4) | NOT NULL |
| total_exact_amount | DECIMAL(10,4) | NOT NULL |
| total_rounded_amount | DECIMAL(10,4) | NOT NULL |
| remainder_amount | DECIMAL(10,4) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL |
| user_id | INT | FK → users(id), NOT NULL |

### Additional Constraints

- CHECK(end_date >= start_date)
- CHECK(total_computed_hours > 0)
- CHECK(total_tip_amount >= 0)

---

## distribution_entries

Stores per-employee results inside a distribution.

| Field | Type | Constraints |
|---|---|---|
| id | INT | PK |
| day_off_count | INT | NOT NULL |
| absence_count | INT | NOT NULL DEFAULT 0 |
| worked_days | INT | NOT NULL |
| computed_hours | DECIMAL(8,2) | NOT NULL |
| exact_amount | DECIMAL(10,4) | NOT NULL |
| rounded_amount | DECIMAL(10,4) | NOT NULL |
| average_daily_hours_snapshot | DECIMAL(5,2) | NOT NULL |
| employee_id | INT | FK → employees(id), NOT NULL |
| distribution_id | INT | FK → distributions(id), NOT NULL |

### Additional Constraints

- UNIQUE(distribution_id, employee_id)

---

# Relationships

- A user can manage many employees.
- An employee can have many absences.
- An employee can have many recurring day offs.
- A distribution belongs to one user.
- A distribution contains many distribution entries.
- Each distribution entry belongs to one employee.
