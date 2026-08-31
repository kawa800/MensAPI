import pytest
import requests
import datetime as dt
from unittest.mock import Mock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from mensapi.scraper.Page import Page 
from mensapi.scraper.Website import Website 
from object_mother import BASE_URL, main_page, iframes, mock_with_test_date

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
    # Act
    iframe_list = iframes()
    # Assert 
    assert len(iframe_list) == 7

def test_day():
    """ The scraper always sorts and returns Monday as the first day in the list """
    iframe_list = iframes()
    assert iframe_list[0].day == "Montag"

# Define in object_mother
def test_date():
    """ The scraper returns the current date """
    mock = mock_with_test_date()
    
    page = Page("https://hauptmensa.de", response=mock)

    assert page.date == "31.08.2026"

