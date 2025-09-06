from agents import function_tool

# Data extracted from https://asunosalon.co.uk on 2025-09-05
# Pricing from pricing-plans.html, Durations from index.html
SERVICES_DATA = {
    "Hair Services": {
        "title": "Hair Dressing & Styling",
        "services": [
            {"name": "Wash & Blow-dry", "price": "From £18", "duration": None},
            {"name": "Wash, Cut & Blow-dry", "price": "From £35", "duration": "45 Minutes"},
            {"name": "Restyle with blow-dry", "price": "From £45", "duration": "30 Minutes"},
            {"name": "Dry hair cut", "price": "From £25", "duration": None},
            {"name": "Dry cut + styling", "price": "From £30", "duration": None},
            {"name": "Extra long or thick hairs", "price": "Extra £5-10", "duration": None},
            {"name": "Root color", "price": "From £35", "duration": None},
            {"name": "Full head color", "price": "From £65", "duration": None},
            {"name": "Full head bleach", "price": "From £150", "duration": None},
            {"name": "Balayage", "price": "From £165", "duration": "2 hrs 15 mins"},
            {"name": "F.H. Highlights", "price": "From £135", "duration": None},
            {"name": "Color correction", "price": "From £150", "duration": None},
            {"name": "Party hair", "price": "From £45", "duration": "2 hrs"},
            {"name": "Loose curls", "price": "From £25", "duration": None},
            {"name": "Loose curls with ½ updo", "price": "From £35", "duration": None},
            {"name": "Tight curls (thin tongs)", "price": "From £35", "duration": None},
            {"name": "Wash & straight blow-dry", "price": "From £25", "duration": None},
            {"name": "Wash & Bouncy blow-dry", "price": "From £30", "duration": None},
            {"name": "Bridal Hair", "price": "From £250", "duration": "2 hrs 35 mins"},
        ]
    },
    "Beauty Treatments": {
        "title": "Beauty Treatments & Head Spa",
        "services": [
            {"name": "Japanese Head Spa", "price": "From £70.00", "duration": "1 hr 50 mins"},
            {"name": "Crystal Clear Dermabrasion", "price": "From £60", "duration": "1 hr"},
            {"name": "Herbal Facial", "price": "From £45", "duration": "1 hr 35 mins"},
            {"name": "Bridal Makeup", "price": "From £350", "duration": None},
            {"name": "Party Makeup", "price": "From £45", "duration": None},
            {"name": "Full Body Waxing", "price": "From £75", "duration": "2 hrs"},
            {"name": "Arm Waxing", "price": "From £15", "duration": None},
            {"name": "Underarms Waxing", "price": "From £5", "duration": None},
            {"name": "Full legs Waxing", "price": "From £20", "duration": None},
            {"name": "½ legs Waxing", "price": "From £10", "duration": None},
            {"name": "Back Waxing", "price": "From £20", "duration": None},
            {"name": "Chest Waxing", "price": "From £15", "duration": None},
            {"name": "Hollywood / bikini line Waxing", "price": "From £20", "duration": "2 hrs 35 mins"},
            {"name": "Stomach Waxing", "price": "From £15", "duration": None},
            {"name": "Chin Waxing", "price": "From £8", "duration": None},
            {"name": "Upper Lip Waxing", "price": "From £2.5", "duration": None},
            {"name": "Full Face Waxing", "price": "From £15", "duration": None},
            {"name": "Neck Waxing", "price": "From £5", "duration": None},
            {"name": "Sides Waxing", "price": "From £3", "duration": None},
            {"name": "Nose Waxing", "price": "From £3", "duration": None},
        ]
    },
    "Nail Services": {
        "title": "Nail Services",
        "services": []
    }
}

@function_tool
def search_services(query: str) -> str:
    """
    Searches for salon services by category from a hardcoded list.
    Returns a formatted list of services with names, prices, and durations.
    Valid categories are: "Hair Services", "Nail Services", "Beauty Treatments".
    """
    
    normalized_category = None
    if "hair" in query.lower():
        normalized_category = "Hair Services"
    elif "beauty" in query.lower():
        normalized_category = "Beauty Treatments"
    elif "nail" in query.lower():
        normalized_category = "Nail Services"

    if not normalized_category or normalized_category not in SERVICES_DATA:
        return f"Sorry, I don't recognize the category '{query}'. Please choose from Hair, Nail, or Beauty services."

    category_data = SERVICES_DATA[normalized_category]
    
    if not category_data["services"]:
        return "Nail services are coming soon to our online booking system! Please check back later."

    title = category_data["title"]
    services = category_data["services"]
    
    results = []
    for s in services:
        duration_str = f" ({s['duration']})" if s['duration'] else ""
        results.append(f"• {s['name']} - {s['price']}{duration_str}")

    return f"✨ {title} ✨\n" + "\n".join(results) + "\nPlease specify the exact service you'd like to book:"
