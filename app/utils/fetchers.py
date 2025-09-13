import requests

def fetch_timetable_html(group_value: str) -> str:
    """
    Fetch the timetable HTML for a given group value.
    Example: group_value='12' fetches o12.html
    """
    url = f"https://podzial.mech.pk.edu.pl/stacjonarne/html/plany/o{group_value}.html"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def fetch_courses_html(url: str = "https://podzial.mech.pk.edu.pl/stacjonarne/html/lista.html") -> str:
    """
    Fetch the HTML content from the given URL (default: lista.html).
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text
