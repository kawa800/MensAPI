import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen 
from urllib.parse import urljoin

from mensapi.api.database import Base
from mensapi.api.database import engine 
from mensapi.scraper.Website import Website
from mensapi.scraper.commit_data import commit_data 

BASE_URL = "https://mocca.stw-d.de/mocca.digitalsignage/3500/Speiseplan3500/"

def test():
    website = Website.from_mensa_url(BASE_URL)
    iframes = website.iframes
    tuesday_iframe = iframes[1]
    res = tuesday_iframe.containers

    with open("out.txt", "w") as file:
        for r in res:
            file.write(r.get_text())

test()

