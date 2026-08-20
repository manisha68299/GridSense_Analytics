-- ==========================================================
-- create_database.sql
-- Run this once, connected as a superuser (e.g. postgres),
-- BEFORE running create_tables.sql.
--
-- Usage:
--   psql -U postgres -f create_database.sql
-- ==========================================================

-- Drop-and-recreate is convenient in dev. In prod you'd never do this —
-- you'd version-control schema changes with a migration tool instead.
DROP DATABASE IF EXISTS green_grid;

CREATE DATABASE green_grid
    WITH
    ENCODING = 'UTF8'
    TEMPLATE = template0;

-- After this runs, reconnect to green_grid before running create_tables.sql:
--   psql -U postgres -d green_grid -f create_tables.sql