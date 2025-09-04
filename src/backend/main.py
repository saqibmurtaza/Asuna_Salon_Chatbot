# backend/main.py

from fastapi import FastAPI, Request, HTTPException, Header
from backend.models import BookingRequest
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# ✅ Load .env variables correctly
load_dotenv()

# ✅ Load secret API key from environment variable
SECRET_KEY = os.getenv("API_SECRET_KEY")

app = FastAPI()

# ✅ Enable CORS (Allow Chainlit frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔐 For production, replace with actual Chainlit domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Booking endpoint with API key validation
@app.post("/booking")
async def create_booking(
    booking: BookingRequest,
    request: Request,
    x_api_key: str = Header(None)
):
    # 🔐 Secure the endpoint
    if x_api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized booking request")

    print("✅ Booking received:", booking)

    # 🚀 Optional: Save to DB (Supabase or other)

    return {
        "message": f"Thanks {booking.name}! Your {booking.service} is booked for {booking.date} at {booking.time}.",
        "status": "success"
    }
