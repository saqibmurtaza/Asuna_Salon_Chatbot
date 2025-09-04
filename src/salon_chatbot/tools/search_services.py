from agents import function_tool
import requests
from bs4 import BeautifulSoup

@function_tool
def search_services(query: str) -> str:
    """
    Searches for salon services on Asuna Salon's official website.
    Returns formatted matching services with names, prices, and descriptions.
    """

    url = "https://asunosalon.co.uk/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all services
        services = soup.select(".services-two__list li")
        results = []

        for service in services:
            name_element = service.select_one(".services-two__services-name h3 a")
            price_element = service.select_one(".services-two__services-price h4")

            name = name_element.text.strip() if name_element else "N/A"
            price = price_element.text.strip() if price_element else "N/A"

            if query.lower() in name.lower():
                results.append(f"**{name}** - {price}")

        if not results:
            return f"Sorry, I couldn't find any services matching '{query}'. You can ask for a full list of services."

        return "Here are the services I found:\n" + "\n".join(results)

    except Exception as e:
        return f"An error occurred while fetching services: {str(e)}"
