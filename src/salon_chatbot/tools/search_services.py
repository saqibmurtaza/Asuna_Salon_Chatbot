from agents import function_tool
from typing import List, Dict
from src.salon_chatbot.salon_data import services

@function_tool
def search_services(query: str) -> List[Dict[str, str]]:
    """
    Searches for salon services from the local data.
    Returns a list of matching services with names, prices, descriptions, and categories.
    """
    if not query or query.lower() == 'all':
        return services

    results = []
    for service in services:
        if query.lower() in service['name'].lower() or query.lower() in service['category'].lower():
            results.append(service)

    return results
