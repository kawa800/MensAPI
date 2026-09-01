import pytest
import requests
from unittest.mock import Mock

from mensapi.scraper.Page import Page 
from mensapi.scraper.Website import Website 
from tests.conftest import BASE_URL

def test_website():
    """ Instantiating a Website returns an object with the same base_url as instance variable """
    # Arrange and Act
    website = Website(BASE_URL)
    # Assert
    assert BASE_URL in str(website)

def test_fetch(main_page):
    """ Fetch returns a Page object containing domain and any subpaths """
    assert "Speiseplan3500" in str(main_page)

def test_get_iframes(iframes):
    """ Fetch the Studierendenwerk Website and return seven iframes """
    assert len(iframes) == 7

def test_day(iframes):
    """ Sort and return Monday as the first day in the list """
    iframe_first_day = iframes[0]
    assert iframe_first_day.day == "Montag"

def test_date(mock_with_test_date):
    """ Return the correct date """
    page = mock_with_test_date
    assert page.date == "31.08.2026"

def test_meals_single_count(schweineschnitzel_mock):
    """ Return one meal if the website contains one meal """
    page = schweineschnitzel_mock
    list_of_meals = page.meals
    assert len(list_of_meals) == 1

def test_meals_single_name(schweineschnitzel_mock):
    """ Return the cleaned string 'Schweineschnitzel mit Paprikacremesauce """
    page = schweineschnitzel_mock
    assert "Schweineschnitzel mit Paprikacremesauce" == page.meals[0]

def test_meals_multiple_count(curryvurst_mock):
    """ Return three meals if the website contains three meals """
    page = curryvurst_mock
    assert len(page.meals) == 3

def test_prices(curryvurst_mock):
    """ Return 2.30, 4.80 and 1.80 for the mock website curryvurst.html """
    page = curryvurst_mock
    list_of_prices = page.prices

    assert page.prices == [2.30, 4.80, 1.80]
