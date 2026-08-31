from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

class Page:

    def __init__(self, url: str, response: requests.Response, parser: str = "html.parser"):
        self.url = url
        self.response = response
        self.soup = BeautifulSoup(response.text, parser)

    @property
    def title(self) -> str | None:
        tag = self.soup.select_one("title")
        return tag.get_text().strip() if tag else None

    @property
    def day(self) -> str | None:
        day = self.soup.find("h2")
        return day.get_text().strip() if day else None
    
    @property
    def date(self) -> str | None: 
        date = self.soup.find("h2").find_next_sibling("p")
        return date.get_text().strip() if date else None

    def select(self, css_selector: str):
        return self.soup.select(css_selector)
    
    def __repr__(self):
        return f"url: {self.url}, status: {self.response.status_code}, title: {self.title}"
