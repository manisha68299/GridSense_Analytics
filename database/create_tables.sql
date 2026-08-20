
CREATE TABLE grids (
    grid_id         SERIAL PRIMARY KEY,
    zone_name       VARCHAR(100) NOT NULL UNIQUE,
    location        VARCHAR(150) NOT NULL,
    max_capacity    NUMERIC(10, 2) NOT NULL CHECK (max_capacity > 0),  -- in kW or MW, defined by whoever seeds the data
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE users (
    user_id         SERIAL PRIMARY KEY,
    username        VARCHAR(50) NOT NULL UNIQUE,
    email           VARCHAR(150) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,   -- never store plaintext passwords
    role            VARCHAR(30) NOT NULL DEFAULT 'operator' CHECK (role IN ('operator', 'manager', 'admin')),
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE grid_readings (
    reading_id      SERIAL PRIMARY KEY,
    grid_id         INTEGER NOT NULL REFERENCES grids(grid_id) ON DELETE CASCADE,
    temperature     NUMERIC(5, 2) NOT NULL,       -- Celsius
    humidity        NUMERIC(5, 2) NOT NULL CHECK (humidity BETWEEN 0 AND 100),
    load_percentage NUMERIC(5, 2) NOT NULL CHECK (load_percentage >= 0),  -- calculated in transform.py
    recorded_at     TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE critical_alerts (
    alert_id        SERIAL PRIMARY KEY,
    grid_id         INTEGER NOT NULL REFERENCES grids(grid_id) ON DELETE CASCADE,
    reading_id      INTEGER REFERENCES grid_readings(reading_id) ON DELETE SET NULL,
    alert_type      VARCHAR(50) NOT NULL,          -- e.g. 'OVERLOAD', 'SPIKE'
    severity        VARCHAR(20) NOT NULL CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    message         TEXT NOT NULL,
    is_resolved     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE alert_logs (
    log_id          SERIAL PRIMARY KEY,
    alert_id        INTEGER NOT NULL REFERENCES critical_alerts(alert_id) ON DELETE CASCADE,
    user_id         INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
    action          VARCHAR(50) NOT NULL,          -- e.g. 'ACKNOWLEDGED', 'RESOLVED', 'ESCALATED'
    notes           TEXT,
    action_at       TIMESTAMP NOT NULL DEFAULT NOW()
);