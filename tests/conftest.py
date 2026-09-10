import pytest
from unittest.mock import Mock
import requests
from pathlib import Path

from mensapi.scraper.Page import Page 
from mensapi.scraper.Website import Website 
from mensapi.scraper.legend import resolve_additive_or_allergen

BASE_URL = "https://mocca.stw-d.de/mocca.digitalsignage/3500/Speiseplan3500/"
HTML_DIR = Path(__file__).parent / "fixtures" / "html"

@pytest.fixture
def main_page() -> Page:
    """ Returns the Page object of the main Studierendenwerk Mensa Website"""
    website = Website(BASE_URL)
    return website.fetch("Index.html")

@pytest.fixture
def iframes() -> list[Page]:
    """ Returns the iFrames embedded in the Studierendenwerk Mensa Website on the 08.09.2026 """
    website = Website(BASE_URL)
    index_html = (HTML_DIR / "index.html").read_text(encoding="utf-8")
    main_page = _construct_mock(index_html)
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

@pytest.fixture
def bolognese_mock() -> Page:
    bolognese_html = (HTML_DIR/ "sauce_bolognese.html").read_text(encoding="utf-8")
    return _construct_mock(bolognese_html)
 
@pytest.fixture
def bolognese_expected_allergens() -> list[dict[str,str]]:
    expected_allergens = [
        {
            "allergen_id": "8",
            "category": "allergens",
            "name": resolve_additive_or_allergen("allergens", 8),
        },
        {
            "allergen_id": "16",
            "category": "allergens",
            "name": resolve_additive_or_allergen("allergens", 16),
        },
        {
            "allergen_id": "20",
            "category": "allergens",
            "name": resolve_additive_or_allergen("allergens", 20),
        },
        {
            "allergen_id": "14",
            "category": "additives",
            "name": resolve_additive_or_allergen("additives", 14),
        },
    ]
    return expected_allergens

