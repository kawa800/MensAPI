import requests
from urllib.parse import urljoin
from mensapi.scraper.Page import Page

class Website:

    def __init__(self, base_url: str, parser: str="html.parser"):
        self.base_url = base_url
        self.session = requests.Session() # Keeps TCP connection open instead of multiple response.get(URL) requests
        self.parser = parser


    def fetch(self, url: str) -> Page:
        """ Fetch a single page """
        full_url = urljoin(self.base_url, url)
        response = self.session.get(full_url)
        response.raise_for_status() # Raise HTTPError if connection fails
        return Page(full_url, response, parser=self.parser)

    def get_iframes(self, page: Page) -> list[Page]:
        """ Find all iFrames on a page and fetch their src """
        pages = []
        for iframe in page.select("iframe"):
            iframe_url = iframe.attrs['src']
            pages.append(self.fetch(iframe_url))

        return pages
    
    def __repr__(self):
        return f"Website-URL: {self.base_url}"

