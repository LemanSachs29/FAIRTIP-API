Logic Model

Table: users
* id                INT PK
* email             VARCHAR(255) NOT NULL UNIQUE
* password_hash     VARCHAR(255) NOT NULL
* created_at        TIMESTAMP NOT NULL

Table: employees
* id                    INT PK
* name                  VARCHAR(100) NOT NULL
* surname               VARCHAR(200) NOT NULL
* average_daily_hours   DECIMAL(5,2) NOT NULL CHECK (average_daily_hours > 0)
* created_at            TIMESTAMP  NOT NULL
* updated_at            TIMESTAMP  NOT NULL
* user_id               INT NOT NULL FK REFERENCES users(id)
 
Table: employee_day_offs
* id            INT PK 
* employee_id   INT NOT NULL FK REFERENCES employees(id)
* weekday       VARCHAR(15) NOT NULL
* UNIQUE (employee_id, weekday)
* CHECK (weekday IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))

Table: absences
* id            INT PK
* date          DATE NOT NULL
* created_at    TIMESTAMP NOT NULL
* employee_id   INT NOT NULL FK REFERENCES employees(id)
* UNIQUE (employee_id, date)

Table: distributions
* id                    INT           PK
* start_date            DATE          NOT NULL
* end_date              DATE          NOT NULL CHECK (end_date >= start_date)
* total_computed_hours  DECIMAL(8,2)  NOT NULL CHECK (total_computed_hours > 0)
* total_tip_amount      DECIMAL(10,4) NOT NULL CHECK (total_tip_amount >= 0)
* tip_per_hour          DECIMAL(10,4) NOT NULL CHECK (tip_per_hour >= 0)
* total_exact_amount    DECIMAL(10,4) NOT NULL CHECK (total_exact_amount >= 0)
* total_roundgited_amount  DECIMAL(10,4) NOT NULL CHECK (total_rounded_amount >= 0)
* remainder_amount      DECIMAL(10,4) NOT NULL CHECK (remainder_amount >= 0)
* created_at            TIMESTAMP     NOT NULL
* user_id               INT NOT NULL FK REFERENCES users(id)


Table: distribution_entries
* id                            INT PK
* day_off_count                 INT NOT NULL CHECK(day_off_count >= 0)
* absence_count                 INT NOT NULL DEFAULT 0 CHECK(absence_count >= 0)
* worked_days                   INT NOT NULL CHECK(worked_days >= 0)
* computed_hours                DECIMAL(8,2) NOT NULL CHECK(computed_hours >= 0)
* exact_amount                  DECIMAL(10, 4) NOT NULL CHECK(exact_amount >= 0)
* rounded_amount                DECIMAL(10, 4) NOT NULL CHECK(rounded_amount >= 0)
* average_daily_hours_snapshot  DECIMAL(5, 2) NOT NULL CHECK(average_daily_hours_snapshot > 0)
* employee_id                   INT NOT NULL FK REFERENCES employees(id)
* distribution_id               INT NOT NULL FK REFERENCES distribution(id)
* UNIQUE (distribution_id, employee_id)