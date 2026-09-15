import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen 
from urllib.parse import urljoin
from mensapi.scraper.Website import Website

BASE_URL = "https://mocca.stw-d.de/mocca.digitalsignage/3500/Speiseplan3500/"

def main():
    website = Website(BASE_URL)
    print(website)

    main_page = website.fetch("Index.html")

    i = 0
    for iframe in website.get_iframes(main_page):
        print(iframe.day)

if __name__ == "__main__":
    main()
