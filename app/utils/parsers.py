from bs4 import BeautifulSoup
from .fetchers import fetch_courses_html

def parse_courses() -> Courses:
    """
    Parse the course list HTML and return a list of dicts with label and value.
    """
    html = fetch_courses_html()
    soup = BeautifulSoup(html, 'html.parser')
    courses = []
    for a in soup.select('#oddzialy a[href^="plany/o"]'):
        label = a.get_text(strip=True)
        href = a.get('href', '')
        value = ''.join(filter(str.isdigit, href))
        courses.append({'label': label, 'value': value})
    return courses
