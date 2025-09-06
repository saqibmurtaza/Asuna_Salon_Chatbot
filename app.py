import chainlit as cl
from salon_chatbot.agents.triage_agent import triage_agent
from salon_chatbot.agents.booking_agent import zara as booking_agent
from salon_chatbot.agents.config_agents import config
from agents import Runner

# --- Persistent Action Buttons ---
persistent_actions = [
    cl.Action(name="explore_services", value="explore_services", label="✨ Our Services", payload={}),
    cl.Action(name="book_appointment", value="book_appointment", label="📅 Book Now", payload={}),
    cl.Action(name="meet_stylists", value="meet_stylists", label="💇‍♀️ Our Team", payload={}),
    cl.Action(name="show_hours", value="show_hours", label="⏰ Hours & Location", payload={}),
    cl.Action(name="contact_us", value="contact_us", label="📞 Contact Us", payload={}),
]

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("agent", triage_agent)
    cl.user_session.set("booking_step", None)

    welcome_message = (
        "🌟 **Welcome to Asuna Salon** 🌟\n\n"
        "Where luxury meets transformation. I'm here to help you discover our exquisite services, "
        "meet our talented stylists, or secure your perfect appointment moment.\n\n"
        "How may I assist you today?"
    )

    await cl.Message(content=welcome_message, actions=persistent_actions).send()

@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    booking_step = cl.user_session.get("booking_step")

    # If user is in a booking flow, route message to booking_agent
    if booking_step:
        agent = booking_agent
        cl.user_session.set("agent", booking_agent)

    result = await Runner.run(agent, input=message.content, run_config=config)
    cl.user_session.set("agent", result.last_agent)

    # Extract metadata from context wrapper
    metadata = getattr(result.context_wrapper, "metadata", {}) or {}
    
    # Update booking_step if included in metadata
    if "booking_step" in metadata:
        cl.user_session.set("booking_step", metadata["booking_step"])

    await cl.Message(content=result.final_output, actions=persistent_actions).send()

# --- Professional Action Callbacks ---

@cl.action_callback("explore_services")
async def on_explore_services(action: cl.Action):
    services = """
**Our Professional Services** ✨

💇 **Hair Services**
• Precision Cutting & Styling
• Creative Coloring & Highlights
• Hair Treatments & Conditioning
• Hair Extensions
• Men's Grooming

💅 **Nail Services** 
• Luxury Manicures
• Spa Pedicures
• Gel Polish & Nail Art
• Nail Extensions

👁️ **Beauty Treatments**
• Eyelash Extensions & Tinting
• Eyebrow Shaping & Henna
• Professional Waxing
• Special Occasion Makeup

*Which service category interests you today?*
"""
    await cl.Message(content=services, actions=persistent_actions).send()
    await action.remove()

@cl.action_callback("book_appointment")
async def on_book_appointment(action: cl.Action):
    # Clear previous context and start fresh
    cl.user_session.set("booking_context", {
        "current_step": "service_selection",
        "collected_data": {},
        "service_confirmed": False,
        "date_confirmed": False, 
        "time_confirmed": False,
        "name_collected": False,
        "booking_reference": None
    })
    
    cl.user_session.set("agent", booking_agent)

    cl.user_session.set("booking_step", "collect_service_category")

    prompt = (
        "Lovely! Let's create your perfect appointment experience 🌸\n"
        "What type of service are you interested in? We specialize in:\n"
        "• Hair Services\n"
        "• Nail Services\n"
        "• Beauty Treatments"

    )
    await cl.Message(content=prompt, actions=persistent_actions).send()
    await action.remove()

@cl.action_callback("meet_stylists")
async def on_meet_stylists(action: cl.Action):
    team_intro = """
**Meet Our Artistic Family** 💫

Our stylists aren't just technicians—they're artists who understand that beauty is personal. Each team member brings unique expertise to ensure your experience is nothing short of exceptional.

"""

    elements = [
        cl.Image(name="emily", display="inline", path="./public/emily.jpg"),
        cl.Text(name="emily_title", content="**Emily Carter**", display="inline"),
        cl.Text(name="emily_bio", content="Creative Director | Color Specialist\n15 years transforming visions into reality with bespoke color techniques", display="block"),
        
        cl.Image(name="james", display="inline", path="./public/james.jpg"),
        cl.Text(name="james_title", content="**James Lee**", display="inline"),
        cl.Text(name="james_bio", content="Master Stylist | Cutting Expert\nRenowned for precision cutting and personalized style consultations", display="block"),
        
        cl.Image(name="sophia", display="inline", path="./public/sophia.jpg"),
        cl.Text(name="sophia_title", content="**Sophia Rodriguez**", display="inline"),
        cl.Text(name="sophia_bio", content="Nail Artist | Wellness Specialist\nCreating miniature masterpieces with attention to detail and care", display="block")
    ]

    await cl.Message(
        content=team_intro,
        elements=elements,
        actions=persistent_actions
    ).send()
    await action.remove()

@cl.action_callback("show_hours")
async def on_show_hours(action: cl.Action):
    hours_location = """
**Visit Our Sanctuary** 🏛️

📍 **Location**
123 Luxury Lane, London SW1A 1AA
*Just moments from Knightsbridge*

⏰ **Opening Hours**
Tuesday - Friday: 9:00 AM – 8:00 PM
Saturday: 9:00 AM – 6:00 PM  
Sunday: 10:00 AM – 4:00 PM
Monday: By appointment only

🚗 **Parking & Transport**
• Complimentary valet parking
• 5-minute walk from Knightsbridge Station
• Bike racks available

*We recommend booking in advance to secure your preferred time*
"""
    await cl.Message(content=hours_location, actions=persistent_actions).send()
    await action.remove()

@cl.action_callback("contact_us")
async def on_contact_us(action: cl.Action):
    contact_info = """
**Connect With Us** 📞

We love hearing from our community and are here to help with any questions.

☎️ **By Phone**
020 7123 4567
*Lines open during salon hours*

📧 **By Email**
hello@asunasalon.co.uk
*We respond within 24 hours*

💬 **In Person**
Visit our salon for a complimentary consultation

📱 **Social Media**
@asunasalon on Instagram & Facebook
*See our latest work and behind-the-scenes moments*

*What's the best way for us to assist you today?*
"""
    await cl.Message(content=contact_info, actions=persistent_actions).send()
    await action.remove()

# --- Enhanced booking flow handler ---
@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="I'd like to book a haircut",
            message="I'm interested in booking a haircut appointment",
            icon="/public/scissors.svg"
        ),
        cl.Starter(
            label="What services do you offer?",
            message="Can you show me your service menu?",
            icon="/public/menu.svg"
        ),
        cl.Starter(
            label="Do you have weekend availability?",
            message="Are you open on weekends for appointments?",
            icon="/public/calendar.svg"
        ),
        cl.Starter(
            label="I need to cancel my appointment",
            message="I need to cancel or reschedule my booking",
            icon="/public/cancel.svg"
        )
    ]
