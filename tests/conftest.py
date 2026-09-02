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
