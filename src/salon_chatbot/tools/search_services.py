from agents import function_tool
import requests
from bs4 import BeautifulSoup

@function_tool
def search_services(query: str) -> str:
    """
    Enhanced search that gracefully handles categories
    """
    query_lower = query.lower()
    
    # Intercept category queries and redirect to appropriate response
    category_responses = {
        "hair services": "For hair services including cutting, coloring, treatments, and extensions, please let me know which specific service you'd like to book using our booking system.",
        "nail services": "For nail services including manicures, pedicures, and nail art, I'd be happy to help you book an appointment. Which specific nail service are you interested in?",
        "beauty treatments": "For beauty treatments like eyelash extensions, eyebrow services, and waxing, let's get you booked in! Which specific treatment would you like?",
        "hair": "Hair services are one of our specialties! We offer cutting, coloring, treatments, and extensions. Would you like to book a specific hair service?",
        "nail": "We offer wonderful nail services including manicures, pedicures, and nail art. Which specific service would you like to explore?",
        "nails": "Our nail services include luxury manicures, spa pedicures, and beautiful nail art. What type of nail service are you looking for?",
        "beauty": "For our beauty treatments including eyelashes, eyebrows, and waxing, I can help you book an appointment. Which specific service interests you?"
    }
    
    if query_lower in category_responses:
        return category_responses[query_lower]


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
