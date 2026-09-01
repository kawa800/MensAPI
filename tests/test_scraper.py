import pytest
import requests
from unittest.mock import Mock

from mensapi.scraper.Page import Page 
from mensapi.scraper.Website import Website 
from tests.conftest import BASE_URL

def test_website():
    """ Instantiating a Website returns an object with the same base_url as instance variable """
    # Arrange 
    # Act
    website = Website(BASE_URL)
    # Assert
    assert BASE_URL in str(website)

def test_fetch(main_page):
    """ Fetch returns a Page object containing domain and any subpaths """
    # Arrange
    # Act
    # Assert
    assert "Speiseplan3500" in str(main_page)

def test_get_iframes(iframes):
    """ Fetching the Studierendenwerk Website returns seven iframes """
    # Arrange
    # Act
    # Assert 
    assert len(iframes) == 7

def test_day(iframes):
    """ The scraper always sorts and returns Monday as the first day in the list """
    iframe_first_day = iframes[0]
    assert iframe_first_day.day == "Montag"

def test_date(mock_with_test_date):
    """ The scraper returns the current date """
    page = Page("https://example.com", response=mock_with_test_date)
    assert page.date == "31.08.2026"

def test_meals_count(schweineschnitzel_mock):
    """ The scraper returns three meals if the website contains three meals """
    page = Page("https://example.com", response=schweineschnitzel_mock)
    meals = page.meals()
    print(meals)
    assert len(meals) == 3
