import requests
from urllib.parse import urljoin
from Page import Page

class Website:

    def __init__(self, base_url: str, parser: str="html.parser"):
        self.base_url = base_url
        self.session = requests.Session() # Keeps TCP connection open instead of multiple response.get(URL) requests
        self.parser = parser


    def fetch(self, url: str) -> Page:
        """ Fetch a page and return Page """
        full_url = urljoin(self.base_url, url)
        response = self.session.get(full_url)
        response.raise_for_status() # Raise HTTPError if connection fails
        return Page(full_url, response, parser=self.parser)
