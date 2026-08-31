import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from mensapi.scraper.Page import Page 
from mensapi.scraper.Website import Website 
from object_mother import BASE_URL, main_page 

def test_website():
    """ Instantiating a Website returns an object with the same base_url as instance variable """
    # Arrange 
    # Act
    website = Website(BASE_URL)
    # Assert
    assert BASE_URL in str(website)

def test_fetch():
    """ Fetch returns a Page object containing domain and any subpaths """
    # Arrange
    # Act
    page = main_page()
    # Assert
    assert "Speiseplan3500" in str(page)

def test_get_iframes():
    """ Fetching the Studierendenwerk Website returns seven iframes """
    # Arrange
    website = Website(BASE_URL)
    main_page = website.fetch("Index.html")
    # Act
    iframes = website.get_iframes(main_page)
    # Assert 
    assert len(iframes) == 7

def test_day():
    """ The scraper always sorts and returns Monday as the first day in the list """
    # Arrange
    website = Website(BASE_URL)
    main_page = website.fetch("Index.html")

    # Act
    iframes = website.get_iframes(main_page)
    first_iframe = iframes[0]

    assert first_iframe.day == "Montag"

def test_date():
    """ The scraper returns the current date """


