import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen 
from urllib.parse import urljoin

from mensapi.api.database import Base
from mensapi.api.database import engine 
from mensapi.scraper.Website import Website
from mensapi.scraper.commit_data import commit_data 

BASE_URL = "https://mocca.stw-d.de/mocca.digitalsignage/3500/Speiseplan3500/"

def main():
    # Ensure the tables in SQLAlchemy are created
    Base.metadata.create_all(bind=engine)

    website = Website.from_mensa_url(BASE_URL)
    scraped_meals = website.weekly_menu
    print(scraped_meals)

    if scraped_meals:
        commit_data(scraped_meals)
    

if __name__ == "__main__":
    main()
