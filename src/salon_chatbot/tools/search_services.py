from agents import function_tool
import requests
from bs4 import BeautifulSoup

from typing import List, Dict

@function_tool
def search_services(query: str) -> List[Dict[str, str]]:
    """
    Searches for salon services on Asuna Salon's official website.
    Returns a list of matching services with names, prices, descriptions, and categories.
    """

    url = "https://asunosalon.co.uk/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        service_sections = soup.select(".services-two__single")

        for section in service_sections:
            category = section.select_one(".services-two__title").text.strip()
            services = section.select(".services-two__list li")

            for service in services:
                name_element = service.select_one(".services-two__services-name h3 a")
                price_element = service.select_one(".services-two__services-price h4")
                description_element = service.select_one(".services-two__services-name p")

                name = name_element.text.strip() if name_element else "N/A"
                price = price_element.text.strip() if price_element else "N/A"
                description = description_element.text.strip() if description_element else ""

                if query.lower() in name.lower() or query.lower() in category.lower():
                    results.append({
                        "name": name,
                        "price": price,
                        "description": description,
                        "category": category
                    })

        return results

    except Exception as e:
        return [{"error": f"An error occurred while fetching services: {str(e)}"}]
