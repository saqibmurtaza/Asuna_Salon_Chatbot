# import chainlit as cl
# from salon_chatbot.agents.triage_agent import triage_agent
# from salon_chatbot.agents.config_agents import config
# from agents import Runner

# # Define the persistent actions that will be available throughout the chat.
# # This list can be reused for multiple messages.
# persistent_actions = [
#     cl.Action(
#         name="explore_services", 
#         value="Explore Our Services", 
#         label="Explore Our Services", 
#         payload={}
#     ),
#     cl.Action(
#         name="book_appointment", 
#         value="Book an Appointment", 
#         label="Book an Appointment",
#         payload={}
#     ),
#     cl.Action(
#         name="meet_stylists", 
#         value="Meet Our Stylists", 
#         label="Meet Our Stylists",
#         payload={}
#     ),
#     cl.Action(
#         name="show_hours", 
#         value="Show Opening Hours", 
#         label="Show Opening Hours",
#         payload={}
#     )
# ]

# @cl.on_chat_start
# async def on_chat_start():
#     """
#     Initializes the chat session and displays the welcome message with persistent actions.
#     """
#     cl.user_session.set("agent", triage_agent)
    
#     welcome_message = (
#         "Welcome to Asuna Salon, where your transformation begins. "
#         "I'm here to guide you through our services or to help you schedule your next moment of luxury. "
#         "If you'd like to connect with our marketing team, just say 'Hi' and I'll put you through.."
#     )
    
#     # Send the welcome message with the persistent actions
#     await cl.Message(content=welcome_message, actions=persistent_actions).send()

# @cl.on_message
# async def on_message(message: cl.Message):
#     """
#     Handles incoming user messages and routes them through the appropriate agent.
#     """
#     agent = cl.user_session.get("agent")
    
#     # Run the agent with the user's message content
#     result = await Runner.run(
#         agent,
#         input=message.content,
#         run_config=config
#     )

#     cl.user_session.set("agent", result.last_agent)
    
#     # Send the agent's response and re-attach the persistent actions
#     await cl.Message(content=result.final_output, actions=persistent_actions).send()

# # --- Action Callbacks ---
# # These functions now have specific logic to handle each button's functionality.

# @cl.action_callback("explore_services")
# async def on_explore_services(action: cl.Action):
#     """
#     Handles the 'Explore Our Services' button click by displaying a list of services.
#     """
#     # In a real app, you would fetch this from a database or salon_tools.py
#     services_list = """
#     Of course! Here are some of our most popular services:
#     - **Luxury Haircut & Style:** Includes a consultation, wash, cut, and professional styling.
#     - **Signature Manicure & Pedicure:** A complete pampering experience for your hands and feet.
#     - **Advanced Hair Coloring:** From balayage to full-color transformations by our expert colorists.
#     - **Revitalizing Spa Facials:** Tailored to your skin type for a radiant glow.

#     Which of these interests you the most?
#     """
#     await cl.Message(content=services_list, actions=persistent_actions).send()
#     # Notify the user that the action was handled
#     await action.remove() # Optional: remove the button after click to prevent re-clicks


# @cl.action_callback("book_appointment")
# async def on_book_appointment(action: cl.Action):
#     """
#     Handles the 'Book an Appointment' button click by guiding the user.
#     """
#     booking_prompt = (
#         "Perfect! To schedule your appointment, could you please let me know: \n"
#         "1. Which service you would like to book? \n"
#         "2. What is your preferred date and time?"
#     )
#     await cl.Message(content=booking_prompt, actions=persistent_actions).send()
#     await action.remove()


# @cl.action_callback("meet_stylists")
# async def on_meet_stylists(action: cl.Action):
#     """Handles the 'Meet Our Stylists' button click by introducing the team with images."""
    
#     # Define the elements with images and text for each stylist
#     elements = [
#         cl.Image(name="Emily", display="inline", path="./public/Emila.jpg"),
#         cl.Text(name="Emily Carter", content="Specializes in creative coloring and modern cuts.", display="inline"),
#         cl.Image(name="James", display="inline", path="./public/anna.jpg"),
#         cl.Text(name="James Lee", content="A master of classic hairstyling and men's grooming.", display="inline"),
#     ]

#     stylist_info = "Our talented team is the heart of Asuna Salon. Here are our lead stylists:"
    
#     # Send the message with the visual elements
#     await cl.Message(
#         content=stylist_info,
#         elements=elements,
#         actions=persistent_actions
#     ).send()
#     await action.remove()


# @cl.action_callback("show_hours")
# async def on_show_hours(action: cl.Action):
#     """Displays the salon's opening hours."""
#     hours_info = """
#     We would be delighted to welcome you during our opening hours:
#     - **Tuesday - Saturday:** 9:00 AM - 7:00 PM
#     - **Sunday:** 10:00 AM - 5:00 PM
#     - **Monday:** Closed

#     Please let me know if you'd like to book an appointment within these times.
#     """
#     await cl.Message(content=hours_info, actions=persistent_actions).send()
#     await action.remove()


from unittest import result
import chainlit as cl
from salon_chatbot.agents.triage_agent import triage_agent
from salon_chatbot.agents.booking_agent import booking_agent
from salon_chatbot.agents.config_agents import config
from agents import Runner

# --- Persistent Action Buttons ---
persistent_actions = [
    cl.Action(name="explore_services", value="explore_services", label="🧖 Explore Services", payload={}),
    cl.Action(name="book_appointment", value="book_appointment", label="📅 Book Appointment", payload={}),
    cl.Action(name="meet_stylists", value="meet_stylists", label="💇‍♀️ Meet Stylists", payload={}),
    cl.Action(name="show_hours", value="show_hours", label="⏰ Opening Hours", payload={}),
]

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("agent", triage_agent)
    cl.user_session.set("booking_step", None)

    welcome_message = (
        "Welcome to Asuna Salon ✨\n"
        "I'm your assistant for discovering services, booking appointments, and more!\n"
        "Let’s begin—how can I help you today?"
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

    # ✅ Extract metadata from context wrapper
    metadata = getattr(result.context_wrapper, "metadata", {}) or {}
    print(f"Metadata: {metadata}")

    # ✅ Update booking_step if included in metadata
    if "booking_step" in metadata:
        cl.user_session.set("booking_step", metadata["booking_step"])

    await cl.Message(content=result.final_output, actions=persistent_actions).send()


# --- Action Callbacks ---

@cl.action_callback("explore_services")
async def on_explore_services(action: cl.Action):
    services = """
Here are some popular services at **Asuna Salon**:

💇‍♀️ **Haircut & Styling** – Modern, classic, or custom.
🎨 **Hair Coloring** – Balayage, highlights, full color.
💅 **Manicure & Pedicure** – With premium polish.
💆‍♀️ **Spa Facial Treatments** – Relax and rejuvenate.

Let me know which one you’re curious about!
"""
    await cl.Message(content=services, actions=persistent_actions).send()
    await action.remove()


@cl.action_callback("book_appointment")
async def on_book_appointment(action: cl.Action):
    cl.user_session.set("agent", booking_agent)
    cl.user_session.set("booking_step", "collect_service")

    prompt = (
        "Great! Let's get you booked 📅\n"
        "**Step 1:** What service would you like to book?"
    )
    await cl.Message(content=prompt, actions=persistent_actions).send()
    await action.remove()


@cl.action_callback("meet_stylists")
async def on_meet_stylists(action: cl.Action):
    elements = [
        cl.Image(name="Emily", display="inline", path="./public/Emila.jpg"),
        cl.Text(name="Emily Carter", content="🎨 Hair Color Specialist | 💇 Women's Cuts", display="inline"),
        cl.Image(name="James", display="inline", path="./public/anna.jpg"),
        cl.Text(name="James Lee", content="✂️ Classic & Modern Styling | 👨 Men's Grooming", display="inline"),
    ]

    await cl.Message(
        content="Meet our amazing team of stylists 💫",
        elements=elements,
        actions=persistent_actions
    ).send()
    await action.remove()


@cl.action_callback("show_hours")
async def on_show_hours(action: cl.Action):
    hours = """
**Salon Opening Hours** ⏰

- **Tuesday - Saturday:** 9:00 AM – 7:00 PM  
- **Sunday:** 10:00 AM – 5:00 PM  
- **Monday:** Closed

Let me know when you'd like to visit!
"""
    await cl.Message(content=hours, actions=persistent_actions).send()
    await action.remove()
