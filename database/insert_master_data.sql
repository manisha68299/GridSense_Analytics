-- ==========================================================
-- insert_master_data.sql
-- Seeds the grids table with sample zones so the ETL pipeline
-- has something real to attach readings to from Step 3 onward.
--
-- Run after create_tables.sql:
--   psql -U postgres -d green_grid -f insert_master_data.sql
-- ==========================================================

INSERT INTO grids (zone_name, location, max_capacity) VALUES
    ('North Zone',        'Durgapur Industrial Park',        500.00),
    ('South Zone',        'Durgapur Residential Sector 4',    350.00),
    ('East Zone',         'Durgapur Commercial Belt',         420.00),
    ('West Zone',         'Durgapur Rural Outskirts',         200.00),
    ('Central Zone',      'Durgapur City Center',             600.00);

-- Optional: seed one admin user so alert_logs has a valid user_id to test with.
-- password_hash below is a placeholder string, NOT a real hash — replace
-- with a proper bcrypt/argon2 hash if you ever wire up real auth.
INSERT INTO users (username, email, password_hash, role) VALUES
    ('admin', 'admin@greengrid.local', 'placeholder_hash_replace_me', 'admin');