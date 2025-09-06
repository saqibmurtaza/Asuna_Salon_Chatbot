from agents import function_tool
import requests
import os
from dotenv import load_dotenv
import chainlit as cl
from typing import Optional
import re
from datetime import datetime

# Load environment variables
load_dotenv()

API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_SECRET = os.getenv("API_SECRET_KEY")

# Complete service menu from Asuna Salon's actual offerings
SALON_SERVICES = {
    "haircut": {"name": "Haircut & Styling", "duration": "45 min", "price": "£28-£35", "category": "hair"},
    "coloring": {"name": "Hair Coloring", "duration": "2-3 hours", "price": "£65-£120", "category": "hair"},
    "treatment": {"name": "Hair Treatment", "duration": "30 min", "price": "£25-£40", "category": "hair"},
    "extensions": {"name": "Hair Extensions", "duration": "3-4 hours", "price": "£150-£300", "category": "hair"},
    "mens": {"name": "Men's Haircut", "duration": "30 min", "price": "£20-£25", "category": "hair"},
    
    "manicure": {"name": "Luxury Manicure", "duration": "45 min", "price": "£25-£35", "category": "nails"},
    "pedicure": {"name": "Spa Pedicure", "duration": "1 hour", "price": "£35-£45", "category": "nails"},
    "gel": {"name": "Gel Nails", "duration": "1 hour", "price": "£30-£40", "category": "nails"},
    "nail-art": {"name": "Nail Art", "duration": "30-60 min", "price": "£10-£25", "category": "nails"},
    
    "eyelashes": {"name": "Eyelash Extensions", "duration": "2 hours", "price": "£60-£100", "category": "beauty"},
    "eyebrows": {"name": "Eyebrow Henna", "duration": "30 min", "price": "£20-£30", "category": "beauty"},
    "waxing": {"name": "Professional Waxing", "duration": "15-45 min", "price": "£12-£35", "category": "beauty"},
    "makeup": {"name": "Makeup Application", "duration": "1 hour", "price": "£35-£50", "category": "beauty"},
    "dermabrasion": {"name": "Crystal Clear Dermabrasion", "duration": "1 hour", "price": "£60", "category": "beauty"},
    "facial": {"name": "Herbal Facial", "duration": "1 hour", "price": "£45", "category": "beauty"}
}

# Add this near the top of your file, after SALON_SERVICES
SERVICE_CATEGORIES = {
    "hair services": ["haircut", "coloring", "treatment", "extensions", "mens"],
    "hair": ["haircut", "coloring", "treatment", "extensions", "mens"],
    "nail services": ["manicure", "pedicure", "gel", "nail-art"],
    "nails": ["manicure", "pedicure", "gel", "nail-art"],
    "nail": ["manicure", "pedicure", "gel", "nail-art"],
    "beauty treatments": ["eyelashes", "eyebrows", "waxing", "makeup", "dermabrasion", "facial"],
    "beauty": ["eyelashes", "eyebrows", "waxing", "makeup", "dermabrasion", "facial"],
    "treatments": ["eyelashes", "eyebrows", "waxing", "makeup", "dermabrasion", "facial"]
}

def initialize_booking_context():
    """Professional booking context initialization"""
    return {
        "current_step": "service_selection",
        "collected_data": {},
        "service_confirmed": False,
        "date_confirmed": False,
        "time_confirmed": False,
        "name_collected": False,
        "booking_reference": None
    }

def store_booking_context(**kwargs):
    """Robust context management"""
    context = cl.user_session.get("booking_context", initialize_booking_context())
    
    for key, value in kwargs.items():
        if value is not None:
            if key in ["service", "date", "time", "name"]:
                context["collected_data"][key] = value
                context[f"{'service' if key == 'service' else key}_confirmed"] = True
            elif key == "current_step":
                context["current_step"] = value
            elif key == "booking_reference":
                context["booking_reference"] = value
    
    cl.user_session.set("booking_context", context)
    return context

@function_tool
def book_appointment(
    service: str = "",
    date: str = "",
    time: str = "",
    name: str = ""
) -> str:
    """
    Professional salon booking system with complete state management
    """
    context = cl.user_session.get("booking_context", initialize_booking_context())
    current_step = context["current_step"]
    collected = context["collected_data"]
    
    # === SERVICE SELECTION ===
        # === SERVICE SELECTION ===
    if current_step == "service_selection":
        if service:
            service_lower = service.lower()
            
            # Handle category selection - SHOW SPECIFIC SERVICES WITH PRICES
            if service_lower in SERVICE_CATEGORIES:
                category_services = []
                for service_id in SERVICE_CATEGORIES[service_lower]:
                    if service_id in SALON_SERVICES:
                        service_data = SALON_SERVICES[service_id]
                        category_services.append(f"• **{service_data['name']}** - {service_data['price']} ({service_data['duration']})")
                
                if category_services:
                    store_booking_context(current_step="service_selection")
                    return (
                        f"✨ **{service.title()}** ✨\n\n"
                        "Here are our available services:\n\n" +
                        "\n".join(category_services) +
                        f"\n\n**Please specify the exact service you'd like to book:**"
                    )
            
            # Handle specific service selection
            for service_id, service_data in SALON_SERVICES.items():
                if service_lower in service_id or service_lower in service_data["name"].lower():
                    store_booking_context(service=service_id, current_step="date_selection")
                    return (
                        f"✅ **{service_data['name']}** selected\n\n"
                        f"*{service_data['duration']} • {service_data['price']}*\n\n"
                        "**When would you like your appointment?**\n"
                        "Please provide your preferred date (YYYY-MM-DD format):"
                    )
            
            # Service not found
            return (
                "I want to ensure we book the perfect service for you! 🌸\n\n"
                "**Please choose from our main categories:**\n"
                "• **Hair Services** - Cutting, coloring, treatments\n"
                "• **Nail Services** - Manicures, pedicures, nail art\n"
                "• **Beauty Treatments** - Eyelashes, facials, waxing\n\n"
                "Or specify the exact service you have in mind."
            )
        
        # Initial service prompt
        return (
            "Lovely! Let's create your perfect appointment experience 🌸\n\n"
            "**What type of service are you interested in?**\n\n"
            "We specialize in:\n"
            "• **Hair Services** - Cutting, coloring, treatments, extensions\n"
            "• **Nail Services** - Manicures, pedicures, nail art\n"
            "• **Beauty Treatments** - Eyelashes, eyebrows, facials, waxing\n\n"
            "Please specify a category or the exact service you'd like to book."
        )
    
    # === DATE SELECTION ===
    elif current_step == "date_selection":
        if date:
            # Validate date format
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date):
                store_booking_context(date=date, current_step="time_selection")
                
                # Get availability from backend
                try:
                    response = requests.get(
                        f"{API_URL}/availability/{date}",
                        headers={"x-api-key": API_SECRET},
                        timeout=5
                    )
                    
                    if response.status_code == 200:
                        available_slots = response.json().get("available_slots", [])
                        if available_slots:
                            return (
                                f"📅 **Available times on {date}:**\n\n" +
                                "\n".join([f"• {slot}" for slot in available_slots]) +
                                "\n\n**Please choose your preferred time:**"
                            )
                except:
                    pass
                
                # Fallback if availability check fails
                return (
                    "⏰ **What time would you prefer?**\n"
                    "Please provide your preferred time (e.g., 14:30):"
                )
            else:
                return "Please provide the date in YYYY-MM-DD format (e.g., 2024-08-24)."
        
        return "**When would you like your appointment?**\nPlease provide your preferred date (YYYY-MM-DD format):"
    
    # === TIME SELECTION ===
    elif current_step == "time_selection":
        if time:
            if re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', time):
                store_booking_context(time=time, current_step="name_collection")
                service_data = SALON_SERVICES.get(collected["service"], {})
                return (
                    f"📋 **Appointment Summary**\n\n"
                    f"**Service:** {service_data.get('name', collected['service'])}\n"
                    f"**Date:** {collected['date']}\n"
                    f"**Time:** {time}\n\n"
                    "**To complete your booking, may I have your name?**"
                )
            else:
                return "Please provide time in HH:MM format (e.g., 14:30)."
        
        return "⏰ **What time would you prefer?**\nPlease provide your preferred time (e.g., 14:30):"
    
    # === NAME COLLECTION ===
    elif current_step == "name_collection":
        if name:
            store_booking_context(name=name, current_step="confirmation")
            
            # Final booking API call
            try:
                service_data = SALON_SERVICES.get(collected["service"], {})
                payload = {
                    "name": name,
                    "contact": "Chatbot Booking",
                    "service": service_data.get("name", collected["service"]),
                    "date": collected["date"],
                    "time": collected["time"]
                }

                response = requests.post(
                    f"{API_URL}/booking",
                    json=payload,
                    headers={"x-api-key": API_SECRET},
                    timeout=10
                )
                
                if response.status_code == 200:
                    response_data = response.json()
                    booking_ref = response_data.get("reference", f"ASU-{datetime.now().strftime('%Y%m%d')}")
                    
                    store_booking_context(booking_reference=booking_ref, current_step="completed")
                    cl.context.metadata["booking_step"] = "confirmed"
                    cl.context.metadata["booking_reference"] = booking_ref
                    
                    return (
                        f"🎉 **Booking Confirmed!** ✨\n\n"
                        f"**Reference:** {booking_ref}\n"
                        f"**Service:** {service_data.get('name', collected['service'])}\n"
                        f"**Date:** {collected['date']}\n"
                        f"**Time:** {collected['time']}\n"
                        f"**Client:** {name}\n\n"
                        f"📞 You'll receive a confirmation 24 hours before your appointment\n"
                        f"⏰ Please arrive 5 minutes early\n"
                        f"❌ 24-hour cancellation policy applies\n\n"
                        f"Thank you for choosing Asuna Salon! 💇‍♀️"
                    )
                
            except Exception as e:
                return (
                    "❌ We're experiencing technical difficulties with our booking system.\n\n"
                    "Please call us at **020 8579 6669** to complete your booking, or try again shortly.\n"
                    "We apologize for the inconvenience."
                )
        
        return "👤 **May I have your name for the booking?**"
    
    return "I'm ready to help you book an appointment! What service are you interested in?"
