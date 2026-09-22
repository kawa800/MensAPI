from __future__ import annotations

import requests
from urllib.parse import urljoin
from mensapi.scraper.Page import Page
from mensapi.scraper.weekday import Weekday
from mensapi.scraper.types import DailyMenu

class Website:


    def __init__(self, base_url: str, iframes: list[Page], parser: str="html.parser"):
        self.iframes = iframes
        self.base_url = base_url
        # self.session = requests.Session() # Keeps TCP connection open instead of multiple response.get(URL) requests
        self.parser = parser

        # MENSA_INDEX_PAGE = self.fetch("Index.html")
        # self.iframes = self.get_iframes(MENSA_INDEX_PAGE) or []

    @classmethod
    def from_mensa_url(cls, base_url: str, parser: str="html.parser") -> Website:
        """ Makes a real GET-Request to the Website of Studierendenwerk """
        session = requests.Session() # Keeps TCP connection open instead of multiple response.get(URL) requests

        def fetch(url: str) -> Page:
            full_url = urljoin(base_url, url)
            response = session.get(full_url)
            response.raise_for_status() # Raise HTTPError if connection fails
            return Page(full_url, response, parser=parser)

        index_page = fetch("Index.html")
        iframes = cls._get_iframes(index_page, fetch)

        return cls(base_url, iframes, parser)


    @classmethod
    def from_html_dir(cls, base_url: str, directory: Path, parser: str = "html.parser") -> "Website":
        """ Read pages from local HTML files instead of the network """
        def fetch(url: str) -> Page:
            file_path = directory / url
            html = file_path.read_text()
            return Page(url, html, parser=parser)

        index_page = fetch("Index.html")
        iframes = cls._get_iframes(index_page, fetch)
        return cls(base_url, iframes, parser)
            

    @staticmethod
    def _order_by_week(page: Page): 
        page_day = page.day
        return Weekday[page_day]

    @staticmethod
    def _get_iframes(index_page: Page, fetch) -> list[Page]:
        """ Find all iFrames on a page and fetch their src.
        Maintains natural order, returning iframe with Monday as first element in list """
        pages = []
        for iframe in index_page.select("iframe"):
            iframe_url = iframe.attrs["src"]
            page = fetch(iframe_url) # Real network-call
            pages.append(page)
        return sorted(pages, key=Website._order_by_week)

    @property
    def weekly_menu(self) -> list[DailyMenu]:
        result = []
        if self.iframes:
            for page in self.iframes:
                for dish in page.complete_dishes:
                    result.append(dish)

        return result
        
    def __repr__(self):
        return f"Website={self.base_url!r}"
