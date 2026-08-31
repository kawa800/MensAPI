from mensapi.scraper.Page import Page 
from mensapi.scraper.Website import Website 


BASE_URL = "https://mocca.stw-d.de/mocca.digitalsignage/3500/Speiseplan3500/"

@staticmethod
def main_page():
    """ Returns the Page object of the main Studierendenwerk Mensa Website"""
    website = Website(BASE_URL)
    return website.fetch("Index.html")
