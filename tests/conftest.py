import pytest
from unittest.mock import Mock
import requests
from pathlib import Path

from mensapi.scraper.Page import Page 
from mensapi.scraper.Website import Website 

BASE_URL = "https://mocca.stw-d.de/mocca.digitalsignage/3500/Speiseplan3500/"
HTML_DIR = Path(__file__).parent / "fixtures" / "html"

@pytest.fixture
def main_page() -> Page:
    """ Returns the Page object of the main Studierendenwerk Mensa Website"""
    website = Website(BASE_URL)
    return website.fetch("Index.html")

@pytest.fixture
def iframes() -> list[Page]:
    """ Returns the iFrames embedded in the Studierendenwerk Mensa Website """
    website = Website(BASE_URL)
    main_page = website.fetch("Index.html")
    return website.get_iframes(main_page)

def _construct_mock(html: str) -> Page:
    mock_response = Mock(spec=requests.Response)
    mock_response.text = html 
    page = Page("https://example.com", response=mock_response)
    return page 
    
@pytest.fixture
def mock_with_test_date() -> Page:
    fake_html = """
        <td>
        <h2>Menuplan</h2>
        <p>31.08.2026</p>
        </td>
    """
    return _construct_mock(fake_html)

@pytest.fixture
def schweineschnitzel_mock() -> Page:
    schweineschnitzel_html = (HTML_DIR/ "schweineschnitzel.html").read_text(encoding="utf-8")
    return _construct_mock(schweineschnitzel_html)

@pytest.fixture
def curryvurst_mock() -> Page:
    curryvurst_html = (HTML_DIR / "curryvurst.html").read_text(encoding="utf-8")
    return _construct_mock(curryvurst_html)

@pytest.fixture
def curryvurst_expected_nutrients() -> list[dict[str,str]]:
    expected_nutrients = [
        {
            "Protein": 17.84,
            "Fat": 30.53,
            "Saturated Fat": 5.13,
            "kcal": 850.65,
            "kJ": 3569.38,
            "Carbohydrates": 120.62,
            "Salt": 7.59,
            "Sugar": 7.25,
        },
        {
            "Protein": 17.04,
            "Fat": 67.63,
            "Saturated Fat": 11.59,
            "kcal": 1143.68,
            "kJ": 4801.19,
            "Carbohydrates": 112.11,
            "Salt": 5.84,
            "Sugar": 28.91,
        },
        {
            "Protein": 18.87,
            "Fat": 14.72,
            "Saturated Fat": 1.54,
            "kcal": 444.59,
            "kJ": 1863.99,
            "Carbohydrates": 53.73,
            "Salt": 6.63,
            "Sugar": 8.68,
        },
    ]
    return expected_nutrients
