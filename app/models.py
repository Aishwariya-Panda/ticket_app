from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class EventBase(SQLModel):
    title: str
    description: str
    venue: str
    date: datetime
    price: float
    image_url: Optional[str] = None
    total_tickets: int = 100

class Event(EventBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reservations: list["Reservation"] = Relationship(back_populates="event")

class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    id: int

class ReservationBase(SQLModel):
    buyer_name: str
    buyer_email: str
    quantity: int = 1

class Reservation(ReservationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    event: Optional[Event] = Relationship(back_populates="reservations")

class ReservationCreate(ReservationBase):
    event_id: int
