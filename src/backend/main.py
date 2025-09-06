# backend/main.py

from fastapi import FastAPI, Request, HTTPException, Header, Depends
from backend.models import BookingRequest, AvailabilityResponse, BookingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from typing import List

# ✅ Load .env variables correctly
load_dotenv()

SECRET_KEY = os.getenv("API_SECRET_KEY")

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo - REPLACE WITH DATABASE IN PRODUCTION
bookings = []

def get_available_slots(target_date: str) -> List[str]:
    """
    Get available time slots for a given date
    Replace this with your actual database query
    """
    # Define business hours and slots
    all_slots = ["09:00", "10:30", "12:00", "14:00", "15:30", "17:00"]
    
    # Get bookings for this date
    date_bookings = [b for b in bookings if b["date"] == target_date]
    booked_times = [b["time"] for b in date_bookings]
    
    # Return available slots
    return [slot for slot in all_slots if slot not in booked_times]

# ✅ Availability endpoint
# Add to your main.py
from datetime import datetime, timedelta

@app.get("/availability/{date_str}", response_model=AvailabilityResponse)
async def get_availability(
    date_str: str,
    x_api_key: str = Header(None)
):
    if x_api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        # Validate date
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        
        if target_date <= today:
            return AvailabilityResponse(
                date=date_str,
                available_slots=[],
                total_slots=0,
                booked_slots=0
            )
        
        # Generate realistic available slots (replace with database)
        all_slots = [
            "09:00", "10:00", "11:00", "12:00", 
            "14:00", "15:00", "16:00", "17:00"
        ]
        
        # Simulate some booked slots (replace with actual database query)
        import random
        booked_count = random.randint(0, 3)
        booked_slots = random.sample(all_slots, booked_count)
        available_slots = [slot for slot in all_slots if slot not in booked_slots]
        
        return AvailabilityResponse(
            date=date_str,
            available_slots=available_slots,
            total_slots=len(all_slots),
            booked_slots=booked_count
        )
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")


# ✅ Enhanced Booking endpoint
@app.post("/booking", response_model=BookingResponse)
async def create_booking(
    booking: BookingRequest,
    request: Request,
    x_api_key: str = Header(None)
):
    # 🔐 Secure the endpoint
    if x_api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Check availability
    available_slots = get_available_slots(booking.date)
    if booking.time not in available_slots:
        raise HTTPException(status_code=400, detail="Time slot not available")

    # Generate booking reference
    booking_ref = f"ASU-{datetime.now().strftime('%Y%m%d')}-{len(bookings)+1:04d}"
    
    # Store booking (replace with database insert)
    booking_data = booking.dict()
    booking_data["reference"] = booking_ref
    bookings.append(booking_data)

    print(f"✅ Booking received: {booking_data}")

    return BookingResponse(
        message=f"Thanks {booking.name}! Your {booking.service} is booked for {booking.date} at {booking.time}.",
        status="success",
        reference=booking_ref
    )
