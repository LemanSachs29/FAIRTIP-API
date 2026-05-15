# Fairtip – Demo Notes

## 1. Introduction

“Fairtip is a restaurant tip distribution system designed for hospitality businesses.

The idea comes from my own experience working in restaurants and beach bars, where tip distribution is often done manually using paper or spreadsheets.”

---

## 2. Problem

“The main problem I wanted to solve was calculating fair tip distributions based on actual worked hours.

The system also takes into account:

* recurring weekly day offs,
* employee absences,
* and different work schedules during the season.”

---

## 3. Tech Stack

### Backend

* Flask
* SQLAlchemy
* PostgreSQL
* JWT Authentication

### Frontend

* React
* Vite

### Deployment

* Railway
* GitHub Pages for API documentation

---

## 4. Database Design

Show:

* conceptual model,
* logical model.

“This is the database design used by the application.

The system is centered around:

* users,
* employees,
* absences,
* day offs,
* distributions,
* and distribution entries.”

Mention:

* relationships,
* constraints,
* decimal precision,
* ownership through user_id.

---

## 5. OpenAPI Documentation

Show:
https://lemansachs29.github.io/FAIRTIP-API/

“This is the OpenAPI documentation for the REST API.

It documents:

* endpoints,
* request bodies,
* responses,
* authentication,
* and schemas.”

---

## 6. Live Application

Show:
https://fairtip-frontend-production.up.railway.app/

---

## 7. Demo Account (Full)

### Dashboard

Explain:

* latest distribution,
* total employees,
* tip per hour,
* recent activity.

### Employees

Explain:

* employee list,
* average daily hours,
* day offs,
* absences.

Open one employee:

* show absence history,
* distribution history.

### Distributions

Open one distribution:
Explain:

* total tip amount,
* computed hours,
* tip per hour,
* rounded amounts,
* remainder handling.

Mention:
“The calculations are based on worked hours during the selected period.”

---

## 8. Demo Account (Clean)

Quickly show:

* create employee,
* add day off,
* add absence,
* create distribution.

---

## 9. Final Notes

“This is currently an MVP focused on the core business logic and backend architecture.

Possible future improvements:

* employee accounts,
* advanced analytics,
* scheduling integration,
* export features,
* and notifications.”
