# from agents import function_tool
# import requests
# import os
# from dotenv import load_dotenv
# import chainlit as cl  # ✅ Add this import

# # ✅ Load environment variables
# load_dotenv()

# API_URL = os.getenv("BACKEND_URL", "http://localhost:8000/booking")
# API_SECRET = os.getenv("API_SECRET_KEY")

# @function_tool
# def book_appointment(name: str, service: str, date: str, time: str) -> str:
#     """
#     Book an appointment for a given service (connected to backend).
#     """
#     payload = {
#         "name": name,
#         "contact": "N/A",  # Optional: Extend later
#         "service": service,
#         "date": date,
#         "time": time
#     }

#     try:
#         response = requests.post(
#             API_URL,
#             json=payload,
#             headers={"x-api-key": API_SECRET}
#         )
#         response.raise_for_status()
#         data = response.json()

#         # ✅ Attach booking step metadata
#         cl.context.metadata["booking_step"] = "confirmed"

#         return data.get("message", "✅ Appointment booked, but no confirmation message returned.")

#     except requests.exceptions.RequestException as e:
#         return f"❌ Network error while booking: {e}"

#     except Exception as e:
#         return f"❌ Unexpected error: {str(e)}"


# src/salon_chatbot/tools/booking_tool.py


from agents import function_tool
import requests
import os
from dotenv import load_dotenv
import chainlit as cl  # ✅ Add this import
from typing import Optional

# --- Helper function to parse and store structured booking data ---
def store_booking_context(name=None, service=None, date=None, time=None):
    context = cl.user_session.get("booking_context") or {}

    if name:
        context["name"] = name
    if service:
        context["service"] = service
    if date:
        context["date"] = date
    if time:
        context["time"] = time

    cl.user_session.set("booking_context", context)
    return context

# --- Booking Tool ---
@function_tool
def book_appointment(
    name: str = "",
    service: str = "",
    date: str = "",
    time: str = ""
) -> str:
    """
    Book an appointment at Asuna Salon.
    Parameters:
    - name: Full name of the person booking
    - service: Service they want (e.g., Manicure)
    - date: Appointment date (YYYY-MM-DD)
    - time: Appointment time (HH:MM)
    """

    # Step 1: Store what the user already gave
    booking = store_booking_context(name, service, date, time)

    # Step 2: Check what info is still missing
    missing = [field for field in ["name", "service", "date", "time"] if not booking.get(field)]

    if missing:
        prompts = {
            "name": "May I have your full name, please?",
            "service": "Which service would you like to book?",
            "date": "What date would you prefer? (e.g., 2025-08-28)",
            "time": "At what time would you like the appointment? (e.g., 14:00)"
        }
        return (
            "To complete your booking, I need the following:\n" +
            "\n".join([f"• {prompts[field]}" for field in missing])
        )

    # Step 3: Confirm final booking message
    name = booking["name"]
    service = booking["service"]
    date = booking["date"]
    time = booking["time"]

    cl.user_session.set("booking_context", {})  # Reset context after completion

    return (
        f"You're all set, {name}! ✨\n"
        f"I've booked your **{service}** on **{date}** at **{time}**.\n"
        f"We look forward to seeing you at Asuna Salon!"
    )
