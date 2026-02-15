from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import select, Session
from datetime import datetime
from typing import List

from .database import init_db, get_session
from .models import Event, EventCreate, Reservation, ReservationCreate

app = FastAPI(title="Ticketing Lite")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def on_start():
    init_db()
    # Seed demo data if empty
    with next(get_session()) as session:
        count = session.exec(select(Event)).first()
        if not count:
            e1 = Event(
                title="Indie Music Night",
                description="An intimate gig with local indie bands.",
                venue="Horizon Club",
                date=datetime.utcnow(),
                price=499.0,
                image_url="https://images.unsplash.com/photo-1518972559570-7cc1309f3229",
                total_tickets=120
            )
            e2 = Event(
                title="Tech Meetup: AI & Web3",
                description="Talks, demos, and networking.",
                venue="T-Hub",
                date=datetime.utcnow(),
                price=0.0,
                image_url="https://images.unsplash.com/photo-1518779578993-ec3579fee39f",
                total_tickets=200
            )
            session.add(e1); session.add(e2)
            session.commit()

# ------------------ Web Pages ------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request, session: Session = Depends(get_session)):
    events = session.exec(select(Event).order_by(Event.date)).all()
    return templates.TemplateResponse("index.html", {"request": request, "events": events})

@app.get("/event/{event_id}", response_class=HTMLResponse)
def event_detail(event_id: int, request: Request, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(404, "Event not found")
    sold = sum(r.quantity for r in event.reservations)
    remaining = max(0, event.total_tickets - sold)
    return templates.TemplateResponse("event_detail.html", {"request": request, "event": event, "remaining": remaining})

@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request, session: Session = Depends(get_session)):
    events = session.exec(select(Event).order_by(Event.date)).all()
    return templates.TemplateResponse("admin.html", {"request": request, "events": events})

@app.post("/admin/create", response_class=RedirectResponse)
def admin_create(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    venue: str = Form(...),
    date: str = Form(...),
    price: float = Form(...),
    image_url: str = Form(""),
    total_tickets: int = Form(100),
    session: Session = Depends(get_session)
):
    dt = datetime.fromisoformat(date)
    event = Event(title=title, description=description, venue=venue, date=dt, price=price, image_url=image_url or None, total_tickets=total_tickets)
    session.add(event)
    session.commit()
    return RedirectResponse(url="/admin", status_code=303)

@app.post("/admin/delete/{event_id}", response_class=RedirectResponse)
def admin_delete(event_id: int, session: Session = Depends(get_session)):
    ev = session.get(Event, event_id)
    if ev:
        session.delete(ev)
        session.commit()
    return RedirectResponse(url="/admin", status_code=303)

# ------------------ API ------------------
@app.get("/api/events", response_model=List[Event])
def api_events(session: Session = Depends(get_session)):
    return session.exec(select(Event).order_by(Event.date)).all()

@app.post("/api/events", response_model=Event)
def api_event_create(payload: EventCreate, session: Session = Depends(get_session)):
    ev = Event(**payload.dict())
    session.add(ev)
    session.commit()
    session.refresh(ev)
    return ev

@app.get("/api/events/{event_id}", response_model=Event)
def api_event_read(event_id: int, session: Session = Depends(get_session)):
    ev = session.get(Event, event_id)
    if not ev: raise HTTPException(404, "Event not found")
    return ev

@app.post("/api/reservations", response_model=Reservation)
def api_reservation(payload: ReservationCreate, session: Session = Depends(get_session)):
    ev = session.get(Event, payload.event_id)
    if not ev: raise HTTPException(404, "Event not found")
    sold = sum(r.quantity for r in ev.reservations)
    remaining = ev.total_tickets - sold
    if payload.quantity < 1 or payload.quantity > remaining:
        raise HTTPException(400, "Invalid quantity or not enough tickets")
    res = Reservation(**payload.dict())
    session.add(res)
    session.commit()
    session.refresh(res)
    return res
