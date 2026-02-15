# Ticketing Lite (Python + FastAPI + Docker)

A lightweight event listing & ticket booking demo inspired by your example link.  
Tech: **FastAPI**, **Jinja2**, **SQLModel (SQLite)**, **Uvicorn**, **HTMX** (progressive enhancement), **Docker**.

## Features
- Home page with upcoming events
- Event detail page with ticket purchase flow (no payment gateway; creates a reservation)
- Admin panel to add/update events
- REST-ish JSON APIs (`/api/events`, `/api/reservations`)
- SQLite db auto-created on first run
- Clean, mobile-friendly UI (vanilla CSS + HTMX)

## Quickstart (Docker)
```bash
# from project root
docker compose up --build
# visit http://localhost:8000
```

## Local (without Docker)
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Admin
- Visit `/admin` to add events (no auth in this demo; add real auth in production).
- Update & delete from the admin list.

## Notes
- This is a demo; no real payments. Extend `/api/reservations` for payments or inventory limits.
- Edit CSS in `app/static/style.css` to customize theme.
