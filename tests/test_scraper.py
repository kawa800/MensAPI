import pytest
import requests
from unittest.mock import Mock
import datetime as dt

from mensapi.scraper.Page import Page 
from mensapi.scraper.Website import Website 
from tests.conftest import BASE_URL

def test_website():
    """ Instantiating a Website returns an object with the same base_url as instance variable """
    # Arrange and Act
    website = Website.from_mensa_url(BASE_URL)
    # Assert
    assert BASE_URL in repr(website)

def test_fetch(main_page):
    """ Fetch returns a Page object containing domain and any subpaths """
    assert "Speiseplan3500" in str(main_page)

def test_get_iframes(iframes):
    """ Fetch the Studierendenwerk Website from 08.09.2026 and check that it returns seven iframes """
    assert len(iframes) == 7

def test_day(iframes):
    """ Fetch the Studierendenwerk Website and check that the first sorted iframe returns Montag """
    iframe_first_day = iframes
    # sorting doesn't work for iframes fixture
    assert iframe_first_day[0].day == "Montag"

@pytest.mark.regression
def test_sorting_bug(iframes):
    iframes = iframes
    website = Website.from_mensa_url(BASE_URL)
    real_iframes = website.iframes
    assert iframes[0].day == real_iframes[0].day

def test_date(mock_with_test_date):
    """ Return the correct date """
    page = mock_with_test_date
    assert str(page.date.date()) == "2026-08-31"

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
    """ Return prices of the mock page: 2.30, 4.80 and 1.80 """
    page = curryvurst_mock

    expected_output =  [
            {"Students": 2.30, "Non-Students": 4.50},
            {"Students": 4.80, "Non-Students": 6.80},
            {"Students": 1.80, "Non-Students": 3.40}
    ]

    assert page.prices == expected_output 

def test_nutrients(curryvurst_mock, curryvurst_expected_nutrients):
    """Return nutritional information for the mock page """
    page = curryvurst_mock
    assert page.nutrients == curryvurst_expected_nutrients

def test_diet(bolognese_mock, bolognese_expected_allergens):
    """ The first dish of the 10.09.2026 is Penne mit Sauce Bolognese and
    it contains the allergens gluten, celery, wheat and the additive beef
    """
    page = bolognese_mock 
    page_first_dish = page.allergens_and_additives[0]
    assert page_first_dish == bolognese_expected_allergens

def test_complete_dishes(bolognese_mock, complete_dishes_bolognese):
    page = bolognese_mock
    page.complete_dishes[0]
    assert page.complete_dishes[0] == complete_dishes_bolognese 

    """ What did I want to test? """
def test_fetch():
    website = Website.from_mensa_url(BASE_URL)
    iframe_days = [frame.day for frame in website.iframes] 
    assert iframe_days == ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

def test_factory():
    website = Website.from_mensa_url(base_url=BASE_URL)
    assert website.iframes[0].day == "Montag" 
