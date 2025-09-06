from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# Model for booking request
class BookingRequest(BaseModel):
    name: str
    contact: str
    service: str
    date: str  # ISO date format
    time: str  # e.g. "14:30"

# Model for availability response
class AvailabilityResponse(BaseModel):
    date: str
    available_slots: List[str]
    total_slots: int
    booked_slots: int

# Model for booking confirmation
class BookingResponse(BaseModel):
    message: str
    status: str
    reference: Optional[str] = None