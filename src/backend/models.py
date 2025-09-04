from pydantic import BaseModel

# Model for booking request
class BookingRequest(BaseModel):
    name: str
    contact: str
    service: str
    date: str  # ISO date format
    time: str  # e.g. "3:00 PM"