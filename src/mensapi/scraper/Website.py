import requests
from urllib.parse import urljoin
from mensapi.scraper.Page import Page
from mensapi.scraper.weekday import Weekday

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

    @staticmethod
    def _order_by_week(page: Page): 
        page_day = page.day

        return Weekday[page_day]


    def get_iframes(self, page: Page) -> list[Page]:
        """ Find all iFrames on a page and fetch their src.
        Maintains natural order, returning iframe with Monday as first element in list """

        pages = []
        for iframe in page.select("iframe"):
            iframe_url = iframe.attrs['src']
            pages.append(self.fetch(iframe_url))

        sorted_pages = sorted(pages, key=self._order_by_week)

        return sorted_pages 
        
    def __repr__(self):
        return f"Website-URL: {self.base_url}"

