from agents import function_tool
from typing import List

from src.salon_chatbot.salon_data import services

@function_tool
def get_service_categories() -> List[str]:
    """
    Returns a list of main service categories from the local data.
    """
    categories = set()
    for service in services:
        categories.add(service['category'])
    return list(categories)
