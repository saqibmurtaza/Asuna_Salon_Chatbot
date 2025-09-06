from agents import function_tool
from typing import List

@function_tool
def get_service_categories() -> List[str]:
    """
    Returns a list of main service categories from the salon's website.
    """
    return ["Hair Dressing", "Head Spa", "Beauty Treatment"]
