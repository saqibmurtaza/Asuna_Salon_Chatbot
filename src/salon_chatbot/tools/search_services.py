from agents import function_tool
import requests
from bs4 import BeautifulSoup

@function_tool
def search_services(query: str) -> str:
    """
    Searches for salon services on Asuna Salon's client site.
    Returns formatted matching services with names, prices, and descriptions.
    """

    url = "https://test-server1.github.io/Asuna-salon-v2/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all services (adapt this based on actual HTML structure)
        services = soup.select(".service-card")
        results = []

        for service in services:
            title = service.select_one(".service-title")
            price = service.select_one(".service-price")
            description = service.select_one(".service-description")

            if not title:
                continue

            full_text = f"{title.text.strip()} {description.text.strip() if description else ''}".lower()
            if query.lower() in full_text:
                results.append(f"💇‍♀️ **{title.text.strip()}** - {price.text.strip() if price else 'Price N/A'}\n{description.text.strip() if description else ''}\n")

        if not results:
            return f"Sorry, I couldn't find any services related to '{query}'. Please try something else."

        return "\n".join(results)

    except Exception as e:
        return f"An error occurred while fetching services: {str(e)}"
