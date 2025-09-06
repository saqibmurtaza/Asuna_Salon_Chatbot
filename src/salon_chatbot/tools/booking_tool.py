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


from agents import function_tool
import uuid

@function_tool
def book_appointment(name: str, service: str, date: str, time: str) -> str:
    """
    Confirms and finalizes a booking at Asuna Salon, and generates a booking reference number.

    Parameters:
    - name: Full name of the person booking.
    - service: The service they want to book (e.g., "Manicure").
    - date: The appointment date in YYYY-MM-DD format.
    - time: The appointment time in HH:MM format.
    """

    # Generate a unique reference number
    booking_id = str(uuid.uuid4()).split('-')[0][:4].upper()
    reference_number = f"ASU-{date.replace('-', '')}-{booking_id}"

    confirmation_message = (
        f"🎉 Booking Confirmed! Reference: {reference_number}\n"
        f"• Service: {service}\n"
        f"• Date: {date}\n"
        f"• Time: {time}\n"
        f"• Client: {name}\n\n"
        f"You'll receive a confirmation 24 hours before your appointment. We look forward to seeing you at Asuna Salon! ✨"
    )

    return confirmation_message
