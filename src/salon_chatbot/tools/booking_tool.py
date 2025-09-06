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
