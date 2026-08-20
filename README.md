# Energy Consumption Analytics & Grid Overload Detection System

## Table of Contents

- [About This Project](#about-this-project)
- [What It Does](#what-it-does)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Folder Structure](#folder-structure)
- [Database Design](#database-design)
- [Setup & Installation](#setup--installation)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Dashboard](#dashboard)
- [Screenshots](#screenshots)
- [Logging & Error Handling](#logging--error-handling)
- [What I'd Add Next](#what-id-add-next)
- [Author](#author)

## About This Project

This is a project I built to understand how a real energy monitoring system might actually work under the hood - not a toy script that runs once on a CSV, but something that keeps running, keeps collecting data, and keeps a database, an API, and a dashboard all in sync with each other.

Grids don't usually fail out of nowhere. Load creeps up, temperatures spike, and a zone gets closer and closer to its limit before anyone notices. The idea here is to catch that early - track weather-driven load per zone continuously, flag anything getting close to overload, and put that in front of someone who can actually act on it, instead of finding out after something trips.

I picked this as my final-year project because it forced me to touch almost every layer a data engineer actually works with: pulling data from an external API, designing a proper relational schema, writing real SQL (window functions, CTEs, views - not just SELECT *), building a REST API around it, and finally making the whole thing usable through a dashboard.

## What It Does

Every 5 minutes, the pipeline:

1. Fetches live weather (temperature, humidity) for 5 grid zones from Open-Meteo's free API
2. Estimates a load percentage for each zone - I don't have access to real smart meter hardware, so this is a synthetic model where load rises as temperature moves away from a comfortable baseline. It's a stand-in for real sensor data, and I'm not pretending otherwise.
3. Writes the reading into PostgreSQL, linked to its zone
4. Runs SQL views that calculate rolling averages and flag zones that are spiking or already critical
5. Exposes all of that through a FastAPI backend
6. Feeds into a Power BI dashboard that updates on refresh

Open the dashboard and you can see, at a glance, which zones are running hot right now and how load has trended over the last few hours.

## Architecture

```
Open-Meteo Weather API
        |
        v
  Python ETL pipeline (data_pipeline/)
  runs every 5 min via APScheduler
        |
        v
  PostgreSQL - green_grid database
  grids, grid_readings, critical_alerts, users, alert_logs
        |
        v
  SQL analytics layer (analytics/)
  window functions, overload detection, views
        |
        v
  FastAPI backend (api/)
  /latest  /critical  /history  /grid/{id}
        |
        v
  Power BI dashboard (dashboard/)
        |
        v
  Grid operator looking at the dashboard
```

A cleaner visual version of this is in `docs/architecture.png`.

## Tech Stack

- **Python 3.11** for the ETL pipeline - Requests for the API call, Pandas for shaping the data
- **APScheduler** to re-run the pipeline every 5 minutes without needing cron or Airflow, which would be overkill for this
- **PostgreSQL** for storage - relational integrity actually matters here since readings belong to zones and alerts belong to readings
- **SQLAlchemy + psycopg2** so nothing gets inserted through raw string-built SQL
- **FastAPI** for the API - the auto-generated Swagger docs alone were worth picking it over Flask, plus request/response validation comes built in through Pydantic
- **Power BI Desktop** for the dashboard, connecting straight to Postgres
- **python-dotenv** so credentials live in `.env`, never hardcoded anywhere
- Python's built-in `logging` module, writing to a rotating file so `logs/pipeline.log` doesn't grow forever

## Folder Structure

```
Energy-Consumption-Analytics-System/
├── data_pipeline/    ETL: config, extract, transform, load, logger, scheduler
├── database/          schema creation, seed data, indexes
├── analytics/          window functions, overload detection, views
├── api/                  FastAPI app, routes, schemas, db connection
├── dashboard/              Power BI file + docs
├── docs/                     diagrams and screenshots
├── logs/                       pipeline.log
├── .env                         (not committed - real credentials go here locally)
├── requirements.txt
├── run.py                        starts the scheduler and the API together
└── README.md
```

## Database Design

Five tables, kept normalized on purpose so I'm not repeating zone info on every single reading row:

- `grids` - the 5 zones, their location, and max capacity
- `grid_readings` - every reading, tied to a grid_id (this is the table that grows every 5 minutes)
- `critical_alerts` - gets a row when a zone crosses the overload threshold, linked back to the exact reading that caused it
- `users` - operators who could act on alerts
- `alert_logs` - who did what, and when, for a given alert

Full ER diagram is in `docs/er_diagram.png`.

## Setup & Installation

**You'll need:** Python 3.11+, PostgreSQL running locally, and Power BI Desktop if you want the dashboard too.

Clone it and set up a virtual environment:

```bash
git clone <repo-url>
cd Energy-Consumption-Analytics-System
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

Fill in `.env` with your actual PostgreSQL credentials:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=green_grid
DB_USER=your_db_username
DB_PASSWORD=your_db_password
```

Then run these SQL files against Postgres, in this order (I use pgAdmin's Query Tool, but psql works too):

```
database/create_tables.sql
database/insert_master_data.sql
database/indexes.sql
```

Followed by the analytics files, also in order since the later ones depend on the views created by the earlier ones:

```
analytics/latest_data_view.sql
analytics/critical_zone_view.sql
analytics/window_functions.sql
analytics/overload_detection.sql
analytics/trend_analysis.sql
analytics/dashboard_queries.sql
```

## Running the Project

Easiest way - one command runs the scheduler and the API together:

```bash
python run.py
```

Or run things separately if you're actively developing:

```bash
python -m data_pipeline.main        # run the ETL once
python -m data_pipeline.scheduler   # run it every 5 minutes
uvicorn api.app:app --reload        # API with hot reload
```

API docs live at `http://127.0.0.1:8000/docs`. For the dashboard, open `dashboard/GridSense.pbix` in Power BI and hit Refresh.

## API Endpoints

| Method | Route | What it returns |
|---|---|---|
| GET | `/` | health check |
| GET | `/latest` | current reading for every zone |
| GET | `/critical` | zones at 80%+ load right now |
| GET | `/history?grid_id=&limit=` | past readings, optionally filtered to one zone |
| GET | `/grid/{grid_id}` | one zone's details plus its latest reading |

## Dashboard

The Power BI file (`dashboard/GridSense.pbix`) has four KPI cards up top (total grids, average load, highest temperature right now, critical zone count), a line chart of load over time per zone, a bar chart comparing zones, a scatter plot of temperature against load, and a table that lists anything currently critical. There are slicers to filter by zone and by date range. More detail on how each visual was built is in `dashboard/dashboard_documentation.md`.

## Screenshots

*(adding these once I capture them)*

| | |
|---|---|
| ![Architecture](docs/architecture.png) | System architecture |
| ![ER Diagram](docs/er_diagram.png) | Database schema |
| ![Dashboard](dashboard/dashboard_design.png) | Power BI dashboard |
| ![API Docs](docs/api_flow.png) | Swagger UI |

## Logging & Error Handling

Every run writes to `logs/pipeline.log` with timestamps and severity levels, so I can go back and see exactly what happened on any given cycle. Failures are handled at a few different levels - if one zone's weather call fails, the other four still go through. If one reading is malformed, it gets skipped instead of failing the whole batch. Network calls and database writes retry automatically a few times with backoff before giving up. And the scheduler itself wraps every run in a try/except, so even something unexpected doesn't quietly kill future scheduled runs.

## What I'd Add Next

- Swap the synthetic load model for real smart meter data if I ever get access to actual sensors
- Add login/auth to the API using the `users` table that's already there
- Deploy this somewhere instead of running it locally - a small VM or a container would do
- Email or SMS alert when a zone actually goes critical, instead of just sitting in a table
- Scale past 5 zones to cover a whole city

## Author

**Manisha Banerjee**
Final-year B.Tech student. Built this to actually practice the full data engineering lifecycle end to end - ETL, database design, SQL analytics, an API, and a dashboard - instead of learning each piece in isolation.