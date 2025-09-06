from agents import function_tool
from typing import List
import random
from datetime import datetime, timedelta

@function_tool
def get_available_slots(service: str, date: str) -> List[str]:
    """
    Returns a list of available time slots for a given service and date.
    This is a mock tool and returns a list of random time slots.
    """

    # Define the salon's opening hours
    opening_time = 10  # 10:00 AM
    closing_time = 18  # 6:00 PM

    # Generate a list of possible time slots
    possible_slots = []
    current_time = datetime.strptime(f"{date} {opening_time}:00", "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(f"{date} {closing_time}:00", "%Y-%m-%d %H:%M")

    while current_time < end_time:
        possible_slots.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=30)

    # Return a random selection of available slots
    if len(possible_slots) > 5:
        return random.sample(possible_slots, 5)
    else:
        return possible_slots
